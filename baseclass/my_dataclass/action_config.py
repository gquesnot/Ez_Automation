from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from baseclass.my_dataclass.coor import Coor
from util.json_function import to_json


@dataclass
class ActionBaseConfig(BaseDataClass, ABC):
    """
    A class to store an action.
    """
    name: str = field(default="")
    delay: float = field(default=.1)
    sleep_after: float = field(default=.1)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionBaseConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class KeyboardActionConfig(ActionBaseConfig):
    """
    A class to store a keyboard action.
    """

    key: str = field(default='')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyboardActionConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class MouseActionConfig(ActionBaseConfig):
    """
    A class to store a mouse action.
    """

    coor: Coor = field(default_factory=Coor)
    region: str = field(default="root")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MouseActionConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class KeyboardActionConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of actions.
    """

    dict: Dict[str, KeyboardActionConfig] = field(default_factory=dict)

    def save(self):
        to_json("keyboardActions", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyboardActionConfigs':
        return from_dict(data_class=cls, data=data)


@dataclass
class MouseActionConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of actions.
    """

    dict: Dict[str, MouseActionConfig] = field(default_factory=dict)

    def save(self):
        to_json("mouseActions", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MouseActionConfigs':
        return from_dict(data_class=cls, data=data)
