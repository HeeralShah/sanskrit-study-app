from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sanskrit_lookup.enums import InputScheme
from sanskrit_lookup.transliteration import (
    convert_detected_slp1_words_to_devanagari,
    is_valid_slp1_token,
    looks_like_slp1_word,
    normalize_to_slp1,
    slp1_to_devanagari,
    slp1_to_iast,
)


class TransliterationTests(unittest.TestCase):
    def test_auto_detects_iast(self) -> None:
        normalized, detected = normalize_to_slp1("\u015biva")
        self.assertEqual(normalized, "Siva")
        self.assertEqual(detected, InputScheme.IAST)

    def test_auto_detects_hk(self) -> None:
        normalized, detected = normalize_to_slp1("ziva")
        self.assertEqual(normalized, "Siva")
        self.assertEqual(detected, InputScheme.HK)

    def test_auto_detects_slp1(self) -> None:
        normalized, detected = normalize_to_slp1("Siva")
        self.assertEqual(normalized, "Siva")
        self.assertEqual(detected, InputScheme.SLP1)

    def test_auto_detects_itrans(self) -> None:
        normalized, detected = normalize_to_slp1("shiva")
        self.assertEqual(normalized, "Siva")
        self.assertEqual(detected, InputScheme.ITRANS)

    def test_auto_detects_devanagari(self) -> None:
        normalized, detected = normalize_to_slp1("\u0936\u093f\u0935")
        self.assertEqual(normalized, "Siva")
        self.assertEqual(detected, InputScheme.DEVANAGARI)

    def test_slp1_display_helpers(self) -> None:
        self.assertEqual(slp1_to_iast("deva"), "deva")
        self.assertEqual(slp1_to_devanagari("deva"), "\u0926\u0947\u0935")

    def test_slp1_token_helpers(self) -> None:
        self.assertTrue(is_valid_slp1_token("agniH"))
        self.assertFalse(is_valid_slp1_token("agni-1"))
        self.assertTrue(looks_like_slp1_word("agniH"))
        self.assertFalse(looks_like_slp1_word("fire"))

    def test_detected_word_conversion_helper(self) -> None:
        converted = convert_detected_slp1_words_to_devanagari("agniH fire gArhapatya")
        self.assertEqual(converted, "\u0905\u0917\u094d\u0928\u093f\u0903 fire \u0917\u093e\u0930\u094d\u0939\u092a\u0924\u094d\u092f")


if __name__ == "__main__":
    unittest.main()
