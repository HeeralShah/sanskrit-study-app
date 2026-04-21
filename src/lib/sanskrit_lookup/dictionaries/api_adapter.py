from __future__ import annotations

import html
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
import httpx

from ..config import API_DICTIONARY_CODES
from ..enums import DictionaryId, LookupStatus
from ..models import DictionaryLookupResult, LookupIssue, NormalizedEntry
from ..transliteration import convert_detected_slp1_words_to_devanagari, slp1_to_devanagari, slp1_to_iast
from .base import DictionaryAdapter

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
MAX_DEFINITIONS = 10
_ENGLISH_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "god",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


class UnimplementedDictionaryAdapter(DictionaryAdapter):
    def __init__(self, dictionary_id: DictionaryId, source_name: str, source_edition: str, message: str | None = None) -> None:
        super().__init__(dictionary_id, source_name, source_edition, implemented=False)
        self.message = message or f"{self.source_name} is declared in the shared dictionary registry but not implemented yet."

    def lookup(self, query_slp1: str, api_base_url: str) -> DictionaryLookupResult:
        issue = LookupIssue(code="not_implemented", message=self.message, dictionary=self.dictionary_id)
        return DictionaryLookupResult(
            dictionary=self.dictionary_id,
            source_name=self.source_name,
            source_edition=self.source_edition,
            status=LookupStatus.NOT_IMPLEMENTED,
            implemented=False,
            issues=[issue],
        )


class CSaltRestDictionaryAdapter(DictionaryAdapter):
    def __init__(self, dictionary_id: DictionaryId, source_name: str, source_edition: str) -> None:
        super().__init__(dictionary_id, source_name, source_edition, implemented=True)
        self.api_dictionary_code = API_DICTIONARY_CODES[dictionary_id]

    def lookup(self, query_slp1: str, api_base_url: str) -> DictionaryLookupResult:
        request_url = self._build_request_url(api_base_url, query_slp1)
        try:
            payload = _fetch_json_payload(request_url)
        except httpx.HTTPStatusError as exc:
            issue = LookupIssue(
                code="api_request_failed",
                message=f"Lookup request to {request_url} returned HTTP {exc.response.status_code}.",
                dictionary=self.dictionary_id,
            )
            return DictionaryLookupResult(
                dictionary=self.dictionary_id,
                source_name=self.source_name,
                source_edition=self.source_edition,
                status=LookupStatus.ERROR,
                implemented=True,
                resolved_source=request_url,
                issues=[issue],
            )
        except Exception as exc:
            issue = LookupIssue(
                code="api_request_failed",
                message=f"Lookup request to {request_url} failed: {exc}",
                dictionary=self.dictionary_id,
            )
            return DictionaryLookupResult(
                dictionary=self.dictionary_id,
                source_name=self.source_name,
                source_edition=self.source_edition,
                status=LookupStatus.ERROR,
                implemented=True,
                resolved_source=request_url,
                issues=[issue],
            )

        raw_entries = payload.get("data", {}).get("entries", [])
        entries = [self._build_entry(raw_entry, request_url) for raw_entry in raw_entries]
        status = LookupStatus.SUCCESS if entries else LookupStatus.NOT_FOUND
        issues: list[LookupIssue] = []
        if not entries:
            issues.append(
                LookupIssue(
                    code="headword_not_found",
                    message=f"No {self.source_name} entries matched the canonical key '{query_slp1}'.",
                    dictionary=self.dictionary_id,
                )
            )
        return DictionaryLookupResult(
            dictionary=self.dictionary_id,
            source_name=self.source_name,
            source_edition=self.source_edition,
            status=status,
            implemented=True,
            resolved_source=request_url,
            entries=entries,
            issues=issues,
        )

    def _build_request_url(self, api_base_url: str, query_slp1: str) -> str:
        query = urllib.parse.urlencode(
            {
                "field": "headword_slp1",
                "query": query_slp1,
                "query_type": "term",
                "size": 20,
            }
        )
        return f"{api_base_url.rstrip('/')}/dicts/{self.api_dictionary_code}/restful/entries?{query}"

    def _build_entry(self, raw_entry: dict[str, object], request_url: str) -> NormalizedEntry:
        raw_xml = str(raw_entry.get("xml", ""))
        xml_element = _parse_xml_record(raw_xml)
        key1 = str(raw_entry.get("headword_slp1") or _find_headword(xml_element) or "")
        key2 = _find_headword_variant(xml_element)
        grammar = _find_grammar(xml_element)
        raw_text = _collapse_text(xml_element)
        top_definitions = _extract_top_definitions(xml_element, raw_text, MAX_DEFINITIONS)
        top_definitions_devanagari = [_convert_sanskrit_words_to_devanagari(item) for item in top_definitions]
        citations = _find_citations(xml_element)
        page_reference = str(raw_entry.get("pageUri") or "") or _find_page_reference(xml_element)

        return NormalizedEntry(
            dictionary=self.dictionary_id,
            source_name=self.source_name,
            source_edition=self.source_edition,
            source_api_url=request_url,
            entry_id=str(raw_entry.get("id") or "") or None,
            page_reference=page_reference or None,
            root_tag=_local_name(xml_element.tag) if xml_element is not None else None,
            canonical_headword=key1,
            headword_slp1=key1,
            headword_iast=slp1_to_iast(key1),
            headword_devanagari=slp1_to_devanagari(key1),
            headword_variants=[key2] if key2 and key2 != key1 else [],
            grammar=grammar or None,
            gloss=raw_text,
            top_definitions=top_definitions,
            top_definitions_devanagari=top_definitions_devanagari,
            citations=citations,
            raw_text=raw_text,
            raw_xml=raw_xml,
            parser_notes=["Normalized from the C-SALT REST `data.entries` payload."],
        )


def _fetch_json_payload(request_url: str) -> dict[str, object]:
    with httpx.Client(timeout=20.0) as client:
        response = client.get(request_url, headers={"User-Agent": "sanskrit-study-app/0.1"})
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("API response was not a dictionary payload.")
        return payload


def _parse_xml_record(raw_xml: str) -> ET.Element | None:
    if not raw_xml:
        return None
    return ET.fromstring(raw_xml)


def _find_headword(node: ET.Element | None) -> str:
    if node is None:
        return ""
    orth = node.find('.//tei:orth[@xml:lang="san-Latn-x-SLP1"]', TEI_NS)
    return _collapse_text(orth)


def _find_headword_variant(node: ET.Element | None) -> str:
    if node is None:
        return ""
    hyph = node.find(".//tei:hyph", TEI_NS)
    return _collapse_text(hyph)


def _find_grammar(node: ET.Element | None) -> str:
    if node is None:
        return ""
    gram = node.find(".//tei:gram", TEI_NS)
    return _collapse_text(gram)


def _find_citations(node: ET.Element | None) -> list[str]:
    if node is None:
        return []
    citations: list[str] = []
    for citation in node.findall('.//tei:cit[@type="literary_source"]', TEI_NS):
        text = _collapse_text(citation)
        if text:
            citations.append(text)
    return citations


def _find_page_reference(node: ET.Element | None) -> str:
    if node is None:
        return ""
    page_ref = node.find('.//tei:note/tei:ref[@type="facs"]', TEI_NS)
    return _collapse_text(page_ref)


def _collapse_text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def _extract_top_definitions(node: ET.Element | None, fallback_text: str, limit: int) -> list[str]:
    if node is not None:
        senses = [_collapse_text(sense) for sense in node.findall(".//tei:sense", TEI_NS)]
    else:
        senses = []
    candidates = senses or [fallback_text]
    definitions: list[str] = []
    for candidate in candidates:
        for part in _split_definition_parts(candidate):
            cleaned = _clean_definition_text(part)
            if cleaned and cleaned not in definitions:
                definitions.append(cleaned)
            if len(definitions) >= limit:
                return definitions
    return definitions


def _split_definition_parts(text: str) -> list[str]:
    if not text:
        return []
    # Apte-style records often use markers like "--2", "--3" inside one long sense.
    parts = re.split(r"\s*--\d+\s*", text)
    return [part for part in parts if part.strip()]


def _clean_definition_text(text: str) -> str:
    if not text:
        return ""
    cleaned = html.unescape(text)
    cleaned = re.sub(r"\[Page[^\]]+\]", " ", cleaned)
    cleaned = re.sub(r"\b\d+,\d+\b", " ", cleaned)
    cleaned = re.sub(r"(?<=\.)(?=[A-Za-z])", " ", cleaned)
    cleaned = cleaned.replace("Âº", "")
    cleaned = " ".join(cleaned.split())
    return cleaned.strip(" -;:,")


def _convert_sanskrit_words_to_devanagari(text: str) -> str:
    return convert_detected_slp1_words_to_devanagari(text, stopwords=_ENGLISH_STOPWORDS, require_case_marker=True)


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag
