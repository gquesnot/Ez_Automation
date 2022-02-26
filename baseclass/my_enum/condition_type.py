from enum import Enum


class ConditionType(str, Enum):
    AND = "AND"
    OR = "OR"
