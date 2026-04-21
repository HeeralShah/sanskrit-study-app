from __future__ import annotations

import json
import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sanskrit_lookup.enums import DictionaryId, LookupStatus
from sanskrit_lookup.lookup import lookup_word


WORDS = {
    "bhed": "Bed",
    "mad": "mad",
    "muk": "muk",
    "paatra": "pAtra",
    "nrp": "nrp",
    "megh": "meG",
}


@contextmanager
def serve_recording_api():
    seen_requests: list[str] = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            seen_requests.append(self.path)
            query = parse_qs(parsed.query)
            headword = query.get("query", [""])[0]
            payload = {
                "data": {
                    "entries": [
                        {
                            "id": f"lemma-{headword or 'empty'}",
                            "headword_slp1": headword,
                            "pageUri": f"mock://{headword}",
                            "xml": (
                                '<entry xmlns="http://www.tei-c.org/ns/1.0">'
                                "<form>"
                                '<orth xml:lang="san-Latn-x-SLP1">'
                                f"{headword}"
                                "</orth>"
                                "</form>"
                                f"<sense>{headword} entry</sense>"
                                "</entry>"
                            ),
                        }
                    ]
                }
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", seen_requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class LookupFixtureTests(unittest.TestCase):
    def test_canonical_queries_and_request_paths_for_sample_words(self) -> None:
        with serve_recording_api() as (api_base_url, seen_requests):
            results = {
                word: lookup_word(word, dictionaries=(DictionaryId.MW,), api_base_url=api_base_url)
                for word in WORDS
            }

        expected_requests = [
            f"/dicts/mw/restful/entries?field=headword_slp1&query={canonical}&query_type=term&size=20"
            for canonical in WORDS.values()
        ]
        self.assertEqual(seen_requests, expected_requests)

        for word, canonical in WORDS.items():
            result = results[word]
            self.assertEqual(result.canonical_query, canonical)
            self.assertEqual(result.status, LookupStatus.SUCCESS)
            self.assertEqual(result.dictionary_results[0].resolved_source, f"{api_base_url}/dicts/mw/restful/entries?field=headword_slp1&query={canonical}&query_type=term&size=20")
            self.assertEqual(result.dictionary_results[0].entries[0].headword_slp1, canonical)
            self.assertEqual(result.dictionary_results[0].entries[0].top_definitions, [f"{canonical} entry"])
            self.assertTrue(result.dictionary_results[0].entries[0].top_definitions_devanagari)

        bhed_entry = results["bhed"].dictionary_results[0].entries[0]
        self.assertEqual(bhed_entry.top_definitions_devanagari[0], "भेद entry")


if __name__ == "__main__":
    unittest.main()
