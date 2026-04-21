from __future__ import annotations

from abc import ABC, abstractmethod
from ..enums import DictionaryId
from ..models import DictionaryLookupResult


class DictionaryAdapter(ABC):
    def __init__(self, dictionary_id: DictionaryId, source_name: str, source_edition: str, implemented: bool) -> None:
        self.dictionary_id = dictionary_id
        self.source_name = source_name
        self.source_edition = source_edition
        self.implemented = implemented

    @abstractmethod
    def lookup(self, query_slp1: str, api_base_url: str) -> DictionaryLookupResult:
        raise NotImplementedError
