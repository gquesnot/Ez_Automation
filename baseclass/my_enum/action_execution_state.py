from enum import Enum


class ActionExecutionState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PRESSED = "PRESSED",
    RELEASED = "RELASED"
