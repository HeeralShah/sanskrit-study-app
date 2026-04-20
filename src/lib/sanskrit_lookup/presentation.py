from __future__ import annotations

from enum import Enum
from typing import Any

from .enums import ResponseStyle
from .models import LookupIssue, NormalizedEntry, NormalizedLookupResult

DEFAULT_MAX_DEFINITION_CHARS = 220
MAX_DEFINITIONS = 10


def format_lookup_result(
    result: NormalizedLookupResult,
    *,
    response_style: ResponseStyle | str = ResponseStyle.COMPACT,
    max_definition_chars: int = DEFAULT_MAX_DEFINITION_CHARS,
) -> dict[str, Any]:
    style = ResponseStyle(response_style)
    if style == ResponseStyle.FULL:
        return result.to_dict()
    return _build_compact_response(result, max_definition_chars=max_definition_chars)


def _build_compact_response(result: NormalizedLookupResult, *, max_definition_chars: int) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str | None, str]] = set()

    for group in result.groups:
        for entry in group.entries:
            key = (_enum_value(entry.dictionary), entry.entry_id, entry.canonical_headword)
            if key in seen:
                continue
            seen.add(key)

            definitions = [_trim_text(item, max_definition_chars) for item in entry.top_definitions][:MAX_DEFINITIONS]
            if not definitions:
                continue

            rows.append(_compact_row(entry, definitions))

    return {
        "query": result.query,
        "canonical_query": result.canonical_query,
        "query_iast": result.query_iast,
        "query_devanagari": result.query_devanagari,
        "status": _enum_value(result.status),
        "results": rows,
        "issues": [_serialize_issue(issue) for issue in result.issues],
    }


def _compact_row(entry: NormalizedEntry, definitions: list[str]) -> dict[str, Any]:
    return {
        "dictionary": _enum_value(entry.dictionary),
        "source_name": entry.source_name,
        "source_edition": entry.source_edition,
        "entry_id": entry.entry_id,
        "headword_slp1": entry.headword_slp1,
        "headword_iast": entry.headword_iast,
        "headword_devanagari": entry.headword_devanagari,
        "headword_variants": entry.headword_variants,
        "page_reference": entry.page_reference,
        "definitions_english": definitions,
    }


def _serialize_issue(issue: LookupIssue) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "code": issue.code,
        "message": issue.message,
    }
    if issue.dictionary is not None:
        payload["dictionary"] = _enum_value(issue.dictionary)
    return payload


def _enum_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value


def _trim_text(text: str, max_length: int) -> str:
    if max_length <= 0 or len(text) <= max_length:
        return text
    return f"{text[: max_length - 1].rstrip()}..."
