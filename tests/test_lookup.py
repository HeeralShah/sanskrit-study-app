from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sanskrit_lookup.enums import DictionaryId, LookupStatus
from sanskrit_lookup.lookup import lookup_word
from support_api_server import serve_test_api


class LookupTests(unittest.TestCase):
    def test_lookup_returns_mw_and_ap90_entries(self) -> None:
        with serve_test_api() as api_base_url:
            result = lookup_word("deva", api_base_url=api_base_url)
            self.assertEqual(result.status, LookupStatus.SUCCESS)
            self.assertEqual(result.dictionaries, [DictionaryId.MW, DictionaryId.AP90])
            self.assertEqual(len(result.groups), 1)
            self.assertEqual(result.groups[0].canonical_headword, "deva")
            self.assertEqual([entry.dictionary for entry in result.groups[0].entries], [DictionaryId.MW, DictionaryId.AP90])
            mw_entry = result.groups[0].entries[0]
            apte_entry = result.groups[0].entries[1]
            self.assertEqual(mw_entry.top_definitions, ["m. a deity, god RV."])
            self.assertEqual(apte_entry.top_definitions[0], "a. divine, celestial Bg. 11.11")

    def test_revised_apte_is_explicitly_unimplemented(self) -> None:
        result = lookup_word("deva", dictionaries=(DictionaryId.AP,))
        self.assertEqual(result.status, LookupStatus.NOT_IMPLEMENTED)
        self.assertEqual(result.dictionary_results[0].status, LookupStatus.NOT_IMPLEMENTED)

    def test_dictionary_order_is_preserved(self) -> None:
        with serve_test_api() as api_base_url:
            result = lookup_word("deva", dictionaries=(DictionaryId.AP90, DictionaryId.MW), api_base_url=api_base_url)
            self.assertEqual([entry.dictionary for entry in result.groups[0].entries], [DictionaryId.AP90, DictionaryId.MW])


if __name__ == "__main__":
    unittest.main()
