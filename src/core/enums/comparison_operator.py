from enum import StrEnum, auto, unique


@unique
class ComparisonOperator(StrEnum):
    eq = auto()
    ne = auto()
    gt = auto()
    ge = auto()
    lt = auto()
    le = auto()
