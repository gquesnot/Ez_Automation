from abc import ABC
from dataclasses import dataclass, field, asdict
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass
from baseclass.my_dataclass.coor import Coor
from baseclass.my_enum.action_execution_state import ActionExecutionState


@dataclass
class BaseActionRecord(BaseDataClass, ABC):
    startAt: float = 0.0
    endAt: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        del res['state']
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'BaseActionRecord':
        return from_dict(data_class=cls, data=data)


@dataclass
class ActionKeyBoardRecord(BaseActionRecord):
    """
    A class to store an action record.
    """
    key: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ActionKeyBoardRecord':
        return from_dict(data_class=cls, data=data)


@dataclass
class ActionMouseClickRecord(BaseActionRecord):
    """
    A class to store an action record.
    """

    coorStart: Coor = field(default_factory=lambda: Coor())

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ActionMouseClickRecord':
        return from_dict(data_class=cls, data=data)


@dataclass
class ActionMouseDragRecord(BaseActionRecord):
    """
    A class to store an action record.
    """

    coorStart: Coor = field(default_factory=lambda: Coor())
    coorEnd: Coor = field(default_factory=lambda: Coor())

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ActionMouseDragRecord':
        return from_dict(data_class=cls, data=data)
