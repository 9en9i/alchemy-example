from enum import StrEnum, auto, unique


@unique
class PublicationType(StrEnum):
    MAGAZINE = auto()
    BOOK = auto()
