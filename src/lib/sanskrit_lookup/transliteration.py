from __future__ import annotations

import re

from .enums import InputScheme


_IAST_DIACRITICS = set("āīūṛṝḷḹṃṁḥṅñṭḍṇśṣ")
_DEVANAGARI_BLOCK = tuple(range(0x0900, 0x0980))
_SLP1_DISTINGUISHERS = set("fFxXEOwWqQPSY")

_IAST_TO_SLP1 = {
    "kh": "K",
    "gh": "G",
    "ch": "C",
    "jh": "J",
    "ṭh": "W",
    "ḍh": "Q",
    "th": "T",
    "dh": "D",
    "ph": "P",
    "bh": "B",
    "ai": "E",
    "au": "O",
    "ā": "A",
    "ī": "I",
    "ū": "U",
    "ṛ": "f",
    "ṝ": "F",
    "ḷ": "x",
    "ḹ": "X",
    "ṃ": "M",
    "ṁ": "M",
    "ḥ": "H",
    "ṅ": "N",
    "ñ": "Y",
    "ṭ": "w",
    "ḍ": "q",
    "ṇ": "R",
    "ś": "S",
    "ṣ": "z",
}

_HK_TO_SLP1 = {
    "kh": "K",
    "gh": "G",
    "ch": "C",
    "jh": "J",
    "Th": "W",
    "Dh": "Q",
    "th": "T",
    "dh": "D",
    "ph": "P",
    "bh": "B",
    "lRR": "X",
    "RR": "F",
    "lR": "x",
    "A": "A",
    "I": "I",
    "U": "U",
    "R": "f",
    "M": "M",
    "H": "H",
    "G": "N",
    "J": "Y",
    "T": "w",
    "D": "q",
    "N": "R",
    "z": "S",
    "S": "z",
}

_ITRANS_TO_SLP1 = {
    "kSh": "kz",
    "j~n": "jY",
    "RRi": "F",
    "R^i": "f",
    "L^i": "x",
    "~N": "N",
    "~n": "Y",
    "aa": "A",
    "ii": "I",
    "uu": "U",
    "Ri": "f",
    "RI": "F",
    "Li": "x",
    "LI": "X",
    "Sh": "z",
    "sh": "S",
    "kh": "K",
    "gh": "G",
    "ch": "C",
    "Ch": "C",
    "jh": "J",
    "Th": "W",
    "Dh": "Q",
    "th": "T",
    "dh": "D",
    "ph": "P",
    "bh": "B",
    "ai": "E",
    "au": "O",
    "M": "M",
    "H": "H",
    "N": "R",
    "T": "w",
    "D": "q",
}

_SLP1_TO_IAST = {
    "a": "a",
    "A": "ā",
    "i": "i",
    "I": "ī",
    "u": "u",
    "U": "ū",
    "f": "ṛ",
    "F": "ṝ",
    "x": "ḷ",
    "X": "ḹ",
    "e": "e",
    "E": "ai",
    "o": "o",
    "O": "au",
    "M": "ṃ",
    "H": "ḥ",
    "k": "k",
    "K": "kh",
    "g": "g",
    "G": "gh",
    "N": "ṅ",
    "c": "c",
    "C": "ch",
    "j": "j",
    "J": "jh",
    "Y": "ñ",
    "w": "ṭ",
    "W": "ṭh",
    "q": "ḍ",
    "Q": "ḍh",
    "R": "ṇ",
    "t": "t",
    "T": "th",
    "d": "d",
    "D": "dh",
    "n": "n",
    "p": "p",
    "P": "ph",
    "b": "b",
    "B": "bh",
    "m": "m",
    "y": "y",
    "r": "r",
    "l": "l",
    "v": "v",
    "S": "ś",
    "z": "ṣ",
    "s": "s",
    "h": "h",
}

SLP1_VOWELS = set("aAiIuUfFxXeEoO")
SLP1_CONSONANTS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh")
SLP1_MARKS = set("MH")
SLP1_ALPHABET = SLP1_VOWELS | SLP1_CONSONANTS | SLP1_MARKS

_SLP1_VOWELS = SLP1_VOWELS
_SLP1_CONSONANTS = SLP1_CONSONANTS

_DEVANAGARI_INDEPENDENT_VOWELS = {
    "अ": "a",
    "आ": "A",
    "इ": "i",
    "ई": "I",
    "उ": "u",
    "ऊ": "U",
    "ऋ": "f",
    "ॠ": "F",
    "ऌ": "x",
    "ॡ": "X",
    "ए": "e",
    "ऐ": "E",
    "ओ": "o",
    "औ": "O",
}

_DEVANAGARI_DEPENDENT_VOWELS = {
    "ा": "A",
    "ि": "i",
    "ी": "I",
    "ु": "u",
    "ू": "U",
    "ृ": "f",
    "ॄ": "F",
    "ॢ": "x",
    "ॣ": "X",
    "े": "e",
    "ै": "E",
    "ो": "o",
    "ौ": "O",
}

_DEVANAGARI_CONSONANTS = {
    "क": "k",
    "ख": "K",
    "ग": "g",
    "घ": "G",
    "ङ": "N",
    "च": "c",
    "छ": "C",
    "ज": "j",
    "झ": "J",
    "ञ": "Y",
    "ट": "w",
    "ठ": "W",
    "ड": "q",
    "ढ": "Q",
    "ण": "R",
    "त": "t",
    "थ": "T",
    "द": "d",
    "ध": "D",
    "न": "n",
    "प": "p",
    "फ": "P",
    "ब": "b",
    "भ": "B",
    "म": "m",
    "य": "y",
    "र": "r",
    "ल": "l",
    "व": "v",
    "श": "S",
    "ष": "z",
    "स": "s",
    "ह": "h",
}

_DEVANAGARI_MARKS = {
    "ं": "M",
    "ः": "H",
    "ँ": "M",
}

_SLP1_TO_DEV_INDEPENDENT_VOWELS = {value: key for key, value in _DEVANAGARI_INDEPENDENT_VOWELS.items()}
_SLP1_TO_DEV_DEPENDENT_VOWELS = {value: key for key, value in _DEVANAGARI_DEPENDENT_VOWELS.items()}
_SLP1_TO_DEV_CONSONANTS = {value: key for key, value in _DEVANAGARI_CONSONANTS.items()}
_SLP1_TO_DEV_MARKS = {value: key for key, value in _DEVANAGARI_MARKS.items()}


def detect_input_scheme(text: str) -> InputScheme:
    text = text.strip()
    if any(ord(char) in _DEVANAGARI_BLOCK for char in text):
        return InputScheme.DEVANAGARI
    if any(char in _IAST_DIACRITICS for char in text.lower()):
        return InputScheme.IAST
    if any(token in text for token in ("RRi", "R^i", "L^i", "~N", "~n", "Sh", "sh", "aa", "ii", "uu")):
        return InputScheme.ITRANS
    if any(char in _SLP1_DISTINGUISHERS for char in text):
        return InputScheme.SLP1
    return InputScheme.HK


def normalize_to_slp1(text: str, input_scheme: InputScheme | str = InputScheme.AUTO) -> tuple[str, InputScheme]:
    scheme = InputScheme(input_scheme)
    if scheme == InputScheme.AUTO:
        scheme = detect_input_scheme(text)
    text = _normalize_query_text(text)
    if scheme == InputScheme.SLP1:
        return text, scheme
    if scheme == InputScheme.IAST:
        return _roman_to_slp1(text, _IAST_TO_SLP1), scheme
    if scheme == InputScheme.HK:
        return _roman_to_slp1(text, _HK_TO_SLP1), scheme
    if scheme == InputScheme.ITRANS:
        return _roman_to_slp1(text, _ITRANS_TO_SLP1), scheme
    if scheme == InputScheme.DEVANAGARI:
        return devanagari_to_slp1(text), scheme
    raise ValueError(f"Unsupported input scheme: {scheme}")


def slp1_to_iast(text: str) -> str:
    return "".join(_SLP1_TO_IAST.get(char, char) for char in text)


def is_valid_slp1_token(text: str) -> bool:
    return bool(text) and all(char in SLP1_ALPHABET for char in text)


def looks_like_slp1_word(
    token: str,
    *,
    stopwords: set[str] | None = None,
    require_case_marker: bool = True,
) -> bool:
    if len(token) < 2:
        return False
    if not token.isalpha():
        return False
    if token.isupper():
        return False
    if stopwords and token.lower() in stopwords:
        return False
    if require_case_marker and not any(char.isupper() for char in token):
        return False
    return is_valid_slp1_token(token)


def convert_detected_slp1_words_to_devanagari(
    text: str,
    *,
    stopwords: set[str] | None = None,
    require_case_marker: bool = True,
) -> str:
    if not text:
        return ""

    def _replace(match: re.Match[str]) -> str:
        token = match.group(0)
        if looks_like_slp1_word(token, stopwords=stopwords, require_case_marker=require_case_marker):
            return slp1_to_devanagari(token)
        return token

    return re.sub(r"[A-Za-z]+", _replace, text)


def slp1_to_devanagari(text: str) -> str:
    output: list[str] = []
    pending_consonant = False
    for char in text:
        if char in _SLP1_CONSONANTS:
            if pending_consonant:
                output.append("्")
            output.append(_SLP1_TO_DEV_CONSONANTS.get(char, char))
            pending_consonant = True
            continue
        if char in _SLP1_VOWELS:
            if pending_consonant:
                if char != "a":
                    output.append(_SLP1_TO_DEV_DEPENDENT_VOWELS[char])
                pending_consonant = False
            else:
                output.append(_SLP1_TO_DEV_INDEPENDENT_VOWELS[char])
            continue
        if char in _SLP1_TO_DEV_MARKS:
            output.append(_SLP1_TO_DEV_MARKS[char])
            pending_consonant = False
            continue
        output.append(char)
        pending_consonant = False
    return "".join(output)


def devanagari_to_slp1(text: str) -> str:
    output: list[str] = []
    pending_consonant = False
    for char in text:
        if char in _DEVANAGARI_INDEPENDENT_VOWELS:
            if pending_consonant:
                output.append("a")
                pending_consonant = False
            output.append(_DEVANAGARI_INDEPENDENT_VOWELS[char])
            continue
        if char in _DEVANAGARI_CONSONANTS:
            if pending_consonant:
                output.append("a")
            output.append(_DEVANAGARI_CONSONANTS[char])
            pending_consonant = True
            continue
        if char in _DEVANAGARI_DEPENDENT_VOWELS:
            if pending_consonant:
                output.append(_DEVANAGARI_DEPENDENT_VOWELS[char])
                pending_consonant = False
            continue
        if char == "्":
            pending_consonant = False
            continue
        if char in _DEVANAGARI_MARKS:
            if pending_consonant:
                output.append("a")
                pending_consonant = False
            output.append(_DEVANAGARI_MARKS[char])
            continue
        if pending_consonant:
            output.append("a")
            pending_consonant = False
        output.append(char)
    if pending_consonant:
        output.append("a")
    return "".join(output)


def _roman_to_slp1(text: str, mapping: dict[str, str]) -> str:
    tokens = sorted(mapping.keys(), key=len, reverse=True)
    output: list[str] = []
    index = 0
    while index < len(text):
        matched = False
        for token in tokens:
            if text[index : index + len(token)] == token:
                output.append(mapping[token])
                index += len(token)
                matched = True
                break
        if matched:
            continue
        output.append(text[index])
        index += 1
    return "".join(output)


def _normalize_query_text(text: str) -> str:
    return " ".join(text.strip().split())
