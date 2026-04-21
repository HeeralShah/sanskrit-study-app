from enum import Enum


class DictionaryId(str, Enum):
    MW = "mw"
    AP = "ap"
    AP90 = "ap90"
    VCP = "vcp"
    BEN = "ben"


class InputScheme(str, Enum):
    AUTO = "auto"
    IAST = "iast"
    HK = "hk"
    SLP1 = "slp1"
    ITRANS = "itrans"
    DEVANAGARI = "devanagari"


class LookupStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    NOT_FOUND = "not_found"
    ERROR = "error"
    NOT_IMPLEMENTED = "not_implemented"


class ResponseStyle(str, Enum):
    FULL = "full"
    COMPACT = "compact"
