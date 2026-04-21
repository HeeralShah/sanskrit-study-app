from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any

from .enums import DictionaryId, InputScheme, LookupStatus


@dataclass
class LookupIssue:
    code: str
    message: str
    dictionary: DictionaryId | None = None


@dataclass
class NormalizedEntry:
    dictionary: DictionaryId
    source_name: str
    source_edition: str
    source_api_url: str | None = None
    source_download_url: str | None = None
    entry_id: str | None = None
    page_reference: str | None = None
    root_tag: str | None = None
    canonical_headword: str = ""
    headword_slp1: str = ""
    headword_iast: str = ""
    headword_devanagari: str = ""
    headword_variants: list[str] = field(default_factory=list)
    grammar: str | None = None
    gloss: str = ""
    top_definitions: list[str] = field(default_factory=list)
    top_definitions_devanagari: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    raw_text: str = ""
    raw_xml: str = ""
    parser_notes: list[str] = field(default_factory=list)


@dataclass
class HeadwordGroup:
    canonical_headword: str
    headword_iast: str
    headword_devanagari: str
    entries: list[NormalizedEntry] = field(default_factory=list)


@dataclass
class DictionaryLookupResult:
    dictionary: DictionaryId
    source_name: str
    source_edition: str
    status: LookupStatus
    implemented: bool
    resolved_source: str | None = None
    entries: list[NormalizedEntry] = field(default_factory=list)
    issues: list[LookupIssue] = field(default_factory=list)


@dataclass
class NormalizedLookupResult:
    query: str
    requested_input_scheme: InputScheme
    detected_input_scheme: InputScheme
    canonical_query: str
    query_iast: str
    query_devanagari: str
    dictionaries: list[DictionaryId]
    status: LookupStatus
    groups: list[HeadwordGroup] = field(default_factory=list)
    dictionary_results: list[DictionaryLookupResult] = field(default_factory=list)
    issues: list[LookupIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def _serialize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _serialize(asdict(value))
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    return value
