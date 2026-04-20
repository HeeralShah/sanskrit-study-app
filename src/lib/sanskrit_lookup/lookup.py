from __future__ import annotations

from collections import OrderedDict
from .config import get_api_base_url
from .dictionaries import get_adapter
from .enums import DictionaryId, InputScheme, LookupStatus
from .models import DictionaryLookupResult, HeadwordGroup, LookupIssue, NormalizedEntry, NormalizedLookupResult
from .transliteration import normalize_to_slp1, slp1_to_devanagari, slp1_to_iast


def lookup_word(
    word: str,
    dictionaries: tuple[DictionaryId | str, ...] = (DictionaryId.MW, DictionaryId.AP90),
    input_scheme: InputScheme | str = InputScheme.AUTO,
    api_base_url: str | None = None,
) -> NormalizedLookupResult:
    requested_scheme = InputScheme(input_scheme)
    normalized_query, detected_scheme = normalize_to_slp1(word, requested_scheme)
    normalized_dictionaries = [_coerce_dictionary_id(dictionary) for dictionary in dictionaries]
    resolved_api_base_url = get_api_base_url(api_base_url)

    dictionary_results: list[DictionaryLookupResult] = []
    issues: list[LookupIssue] = []
    for dictionary_id in normalized_dictionaries:
        result = get_adapter(dictionary_id).lookup(normalized_query, resolved_api_base_url)
        dictionary_results.append(result)
        issues.extend(result.issues)

    groups = _build_groups(dictionary_results)
    status = _derive_status(groups, dictionary_results)

    return NormalizedLookupResult(
        query=word,
        requested_input_scheme=requested_scheme,
        detected_input_scheme=detected_scheme,
        canonical_query=normalized_query,
        query_iast=slp1_to_iast(normalized_query),
        query_devanagari=slp1_to_devanagari(normalized_query),
        dictionaries=normalized_dictionaries,
        status=status,
        groups=groups,
        dictionary_results=dictionary_results,
        issues=issues,
    )


def _coerce_dictionary_id(dictionary: DictionaryId | str) -> DictionaryId:
    if isinstance(dictionary, DictionaryId):
        return dictionary
    return DictionaryId(dictionary)


def _build_groups(dictionary_results: list[DictionaryLookupResult]) -> list[HeadwordGroup]:
    grouped: OrderedDict[str, list[NormalizedEntry]] = OrderedDict()
    for result in dictionary_results:
        for entry in result.entries:
            grouped.setdefault(entry.canonical_headword, []).append(entry)

    groups: list[HeadwordGroup] = []
    for canonical_headword, entries in grouped.items():
        first_entry = entries[0]
        groups.append(
            HeadwordGroup(
                canonical_headword=canonical_headword,
                headword_iast=first_entry.headword_iast,
                headword_devanagari=first_entry.headword_devanagari,
                entries=entries,
            )
        )
    return groups


def _derive_status(groups: list[HeadwordGroup], dictionary_results: list[DictionaryLookupResult]) -> LookupStatus:
    statuses = {result.status for result in dictionary_results}
    if groups:
        if statuses == {LookupStatus.SUCCESS}:
            return LookupStatus.SUCCESS
        return LookupStatus.PARTIAL
    if statuses == {LookupStatus.NOT_IMPLEMENTED}:
        return LookupStatus.NOT_IMPLEMENTED
    if LookupStatus.ERROR in statuses:
        return LookupStatus.ERROR
    if LookupStatus.NOT_IMPLEMENTED in statuses:
        return LookupStatus.PARTIAL
    return LookupStatus.NOT_FOUND
