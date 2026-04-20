from __future__ import annotations

from ..config import EDITIONS, SOURCE_NAMES
from ..enums import DictionaryId
from .api_adapter import CSaltRestDictionaryAdapter, UnimplementedDictionaryAdapter


_ADAPTERS = {
    DictionaryId.MW: CSaltRestDictionaryAdapter(
        dictionary_id=DictionaryId.MW,
        source_name=SOURCE_NAMES[DictionaryId.MW],
        source_edition=EDITIONS[DictionaryId.MW],
    ),
    DictionaryId.AP: UnimplementedDictionaryAdapter(
        dictionary_id=DictionaryId.AP,
        source_name=SOURCE_NAMES[DictionaryId.AP],
        source_edition=EDITIONS[DictionaryId.AP],
        message="The revised Apte 1957 dictionary is not currently wired to a documented C-SALT REST dictionary code in this repo.",
    ),
    DictionaryId.AP90: CSaltRestDictionaryAdapter(
        dictionary_id=DictionaryId.AP90,
        source_name=SOURCE_NAMES[DictionaryId.AP90],
        source_edition=EDITIONS[DictionaryId.AP90],
    ),
    DictionaryId.VCP: UnimplementedDictionaryAdapter(
        dictionary_id=DictionaryId.VCP,
        source_name=SOURCE_NAMES[DictionaryId.VCP],
        source_edition=EDITIONS[DictionaryId.VCP],
    ),
    DictionaryId.BEN: UnimplementedDictionaryAdapter(
        dictionary_id=DictionaryId.BEN,
        source_name=SOURCE_NAMES[DictionaryId.BEN],
        source_edition=EDITIONS[DictionaryId.BEN],
    ),
}


def get_adapter(dictionary_id: DictionaryId):
    return _ADAPTERS[dictionary_id]


def list_supported_dictionaries() -> list[DictionaryId]:
    return list(_ADAPTERS.keys())
