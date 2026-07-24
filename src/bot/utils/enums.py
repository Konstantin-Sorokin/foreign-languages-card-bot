from enum import StrEnum


class VerbGroup(StrEnum):
    UNCHANGED = "unchanged"
    TD = "td"
    VOWEL = "vowel"
    STRONG = "strong"


class PackKind(StrEnum):
    CATEGORY = "category"
    SET = "set"


class ContentType(StrEnum):
    MOVIE = "movie"
    SERIES = "series"
    BOOK = "book"
    STUDY = "study"


class PackAction(StrEnum):
    OPEN = "open"
    BACK = "back"
    ADD = "add"
