from __future__ import annotations

import argparse
import json

from lib.sanskrit_lookup.enums import DictionaryId, InputScheme, ResponseStyle
from lib.sanskrit_lookup.lookup import lookup_word
from lib.sanskrit_lookup.presentation import DEFAULT_MAX_DEFINITION_CHARS, format_lookup_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lookup Sanskrit headwords across normalized dictionary adapters.")
    parser.add_argument("--word", required=True, help="Headword to search for.")
    parser.add_argument(
        "--dictionary",
        dest="dictionaries",
        action="append",
        choices=[dictionary.value for dictionary in DictionaryId],
        help="Dictionary id to query. Repeat to query multiple dictionaries. Defaults to mw and ap90.",
    )
    parser.add_argument(
        "--input-scheme",
        default=InputScheme.AUTO.value,
        choices=[scheme.value for scheme in InputScheme],
        help="Interpretation of the input headword.",
    )
    parser.add_argument(
        "--api-base-url",
        default=None,
        help="Optional override for the Sanskrit lookup API base URL.",
    )
    parser.add_argument(
        "--response-style",
        default=ResponseStyle.COMPACT.value,
        choices=[style.value for style in ResponseStyle],
        help="Response shape to emit. 'compact' is plugin-friendly; 'full' includes grouped/raw fields.",
    )
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation to use for stdout output.")
    parser.add_argument(
        "--full-output",
        action="store_true",
        help="Legacy shortcut for --response-style full.",
    )
    parser.add_argument(
        "--max-definition-chars",
        type=int,
        default=DEFAULT_MAX_DEFINITION_CHARS,
        help="Trim each definition line to this many characters in compact mode.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    dictionaries = tuple(args.dictionaries or [DictionaryId.MW.value, DictionaryId.AP90.value])
    result = lookup_word(
        word=args.word,
        dictionaries=dictionaries,
        input_scheme=args.input_scheme,
        api_base_url=args.api_base_url,
    )
    response_style = ResponseStyle.FULL if args.full_output else ResponseStyle(args.response_style)
    payload = format_lookup_result(
        result,
        response_style=response_style,
        max_definition_chars=args.max_definition_chars,
    )
    print(json.dumps(payload, indent=args.indent))

