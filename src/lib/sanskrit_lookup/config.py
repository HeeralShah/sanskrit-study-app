from __future__ import annotations

import os

from .enums import DictionaryId

DEFAULT_API_BASE_URL = "https://api.c-salt.uni-koeln.de"

EDITIONS = {
    DictionaryId.MW: "Monier-Williams Sanskrit-English Dictionary, 1899",
    DictionaryId.AP: "Apte Practical Sanskrit-English Dictionary, revised edition, 1957",
    DictionaryId.AP90: "Apte Practical Sanskrit-English Dictionary, 1890",
    DictionaryId.VCP: "Vacaspatyam",
    DictionaryId.BEN: "Benfey Sanskrit-English Dictionary",
}

SOURCE_NAMES = {
    DictionaryId.MW: "Monier-Williams",
    DictionaryId.AP: "Apte",
    DictionaryId.AP90: "Apte",
    DictionaryId.VCP: "Vacaspatyam",
    DictionaryId.BEN: "Benfey",
}

API_DICTIONARY_CODES = {
    DictionaryId.MW: "mw",
    DictionaryId.AP90: "ap90",
}


def get_api_base_url(override: str | None = None) -> str:
    if override is not None:
        return override
    return os.environ.get("SANSKRIT_LOOKUP_API_BASE_URL", DEFAULT_API_BASE_URL)
