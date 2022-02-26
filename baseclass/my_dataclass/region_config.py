from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from baseclass.my_dataclass.rectangle import Rectangle
from util.json_function import toJson


@dataclass
class RegionConfig(BaseDataClass):
    """
    A class to store a region.
    """
    name: str = field(default="")
    rectangle: Rectangle = field(default_factory=Rectangle)
    ratio: float = field(default=1.0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'RegionConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class RegionConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of regions.
    """

    dict: Dict[str, RegionConfig] = field(default_factory=dict)

    def save(self):
        toJson("regions", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'RegionConfigs':
        return from_dict(data_class=cls, data=data)
