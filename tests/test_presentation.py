from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.sanskrit_lookup.lookup import lookup_word
from lib.sanskrit_lookup.presentation import format_lookup_result
from support_api_server import serve_test_api


class PresentationTests(unittest.TestCase):
    def test_compact_shape_is_emitted_without_group_payload(self) -> None:
        with serve_test_api() as api_base_url:
            result = lookup_word("deva", api_base_url=api_base_url)
            payload = format_lookup_result(result, response_style="compact", max_definition_chars=10)

        self.assertEqual(payload["canonical_query"], "deva")
        self.assertNotIn("groups", payload)
        self.assertEqual(payload["results"][0]["dictionary"], "mw")
        self.assertIn("definitions_english", payload["results"][0])
        self.assertTrue(payload["results"][0]["definitions_english"][0].endswith("..."))

    def test_full_shape_matches_model_serialization(self) -> None:
        with serve_test_api() as api_base_url:
            result = lookup_word("deva", api_base_url=api_base_url)
            payload = format_lookup_result(result, response_style="full")

        self.assertIn("groups", payload)
        self.assertIn("dictionary_results", payload)
        self.assertEqual(payload["status"], "success")


if __name__ == "__main__":
    unittest.main()
