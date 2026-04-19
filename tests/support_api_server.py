from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


MW_RESPONSE = {
    "data": {
        "entries": [
            {
                "created": "2025-06-30T14:13:34.125685",
                "id": "lemma-deva",
                "headword_slp1": "deva",
                "xml": '<entry xmlns="http://www.tei-c.org/ns/1.0" xml:id="lemma-deva" ana="H1"><form><orth ana="key1" xml:lang="san-Latn-x-SLP1">deva</orth><hyph ana="key2" xml:lang="san-Latn-x-SLP1-headword">dev/a</hyph></form><sense><gramGrp><gram ana="lex">m.</gram></gramGrp>a deity, god <cit type="literary_source"><bibl><ref target="#rv">RV.</ref></bibl></cit><note><ref target="#page-0492" type="facs">492,2</ref></note></sense></entry>',
            }
        ]
    }
}

AP90_RESPONSE = {
    "data": {
        "entries": [
            {
                "created": "2025-06-30T14:13:34.125685",
                "id": "lemma_deva_15626",
                "headword_slp1": "deva",
                "pageUri": "http://images.cceh.uni-koeln.de/sanskrit/ap90/pg_0578.pdf",
                "xml": '<entry xmlns="http://www.tei-c.org/ns/1.0" xml:id="lemma_deva_15626"><form><orth notation="transliterated" type="lemma" xml:lang="san-Latn-x-SLP1">deva</orth></form><sense><hi rendition="#i">a.</hi> divine, celestial <cit type="literary_source"><bibl><ref target="#bg">Bg. 11.11</ref></bibl></cit></sense></entry>',
            }
        ]
    }
}

EMPTY_RESPONSE = {"data": {"entries": []}}


@contextmanager
def serve_test_api():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            key = query.get("query", [""])[0]
            dictionary = _dictionary_code(parsed.path)
            payload = _payload_for(dictionary, key)
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
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _dictionary_code(path: str) -> str:
    parts = [part for part in path.strip("/").split("/") if part]
    return parts[1] if len(parts) >= 2 and parts[0] == "dicts" else ""


def _payload_for(dictionary: str, key: str) -> dict[str, object]:
    if key != "deva":
        return EMPTY_RESPONSE
    if dictionary == "mw":
        return MW_RESPONSE
    if dictionary == "ap90":
        return AP90_RESPONSE
    return EMPTY_RESPONSE
