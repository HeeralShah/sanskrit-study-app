from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sanskrit_lookup.dictionaries.api_adapter import (  # noqa: E402
    _convert_sanskrit_words_to_devanagari,
    _extract_top_definitions,
)


class DictionaryParsingTests(unittest.TestCase):
    def test_extracts_and_limits_top_definitions(self) -> None:
        xml = ET.fromstring(
            '<entry xmlns="http://www.tei-c.org/ns/1.0">'
            "<sense>--1 agniH fire --2 deva god --3 gArhapatya ritual fire "
            "--4 AhavanIya form --5 dakziRa fire --6 agnihotra offering "
            "--7 agnikarman action --8 agniSAlA sanctuary --9 agniD priest "
            "--10 agnikuRqa vessel --11 agniparIkzA ordeal</sense>"
            "</entry>"
        )
        definitions = _extract_top_definitions(xml, "", 10)
        self.assertEqual(len(definitions), 10)
        self.assertEqual(definitions[0], "agniH fire")
        self.assertEqual(definitions[-1], "agnikuRqa vessel")

    def test_converts_detected_slp1_words_in_definition(self) -> None:
        converted = _convert_sanskrit_words_to_devanagari("agniH fire gArhapatya deva")
        self.assertEqual(converted, "अग्निः fire गार्हपत्य deva")


if __name__ == "__main__":
    unittest.main()
