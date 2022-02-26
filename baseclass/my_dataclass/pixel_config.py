from dataclasses import dataclass, field
from typing import List, Dict, Any

from dacite import from_dict, Config

from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from baseclass.my_dataclass.pixel import Pixel
from baseclass.my_enum.condition_type import ConditionType
from util.json_function import toJson


@dataclass
class PixelConfig(BaseDataClass):
    """
    A class to store a pixel List with relation.
    """
    name: str = field(default="")
    type: ConditionType = field(default="OR")
    pixels: List[Pixel] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'PixelConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class PixelConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of pixel.
    """

    dict: Dict[str, PixelConfig] = field(default_factory=dict)

    def save(self):
        toJson("pixel", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PixelConfigs':
        return from_dict(data_class=cls, data=data, config=Config(cast=[ConditionType]))
