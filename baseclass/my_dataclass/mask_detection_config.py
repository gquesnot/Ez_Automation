from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from baseclass.my_dataclass.color import Color
from util.json_function import toJson


@dataclass
class MaskDetectionConfig(BaseDataClass):
    """
    A class to store a mask detection.
    """

    name: str = field(default="")
    draw: bool = field(default=False)
    lower: Color = field(default=Color(0, 0, 0))
    upper: Color = field(default=Color(0, 0, 0))
    maxFound: int = field(default=1)
    kernelSize: int = field(default=3)
    minArea: int = field(default=0)
    drawColor: Color = field(default=Color(255, 0, 0))
    drawSize: int = field(default=1)
    track: bool = field(default=False)
    region: str = field(default="root")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MaskDetectionConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class MaskDetectionConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of mask detection.
    """

    def save(self):
        toJson("maskDetection", self.to_dict())

    dict: Dict[str, MaskDetectionConfig] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MaskDetectionConfigs':
        return from_dict(data_class=cls, data=data)
