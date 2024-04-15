from enum import StrEnum, auto, unique


@unique
class ComparisonOperator(StrEnum):
    eq: str = auto()
    ne: str = auto()
    gt: str = auto()
    ge: str = auto()
    lt: str = auto()
    le: str = auto()
