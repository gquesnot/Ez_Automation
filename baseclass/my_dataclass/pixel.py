from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass
from baseclass.my_dataclass.color import Color
from baseclass.my_dataclass.coor import Coor


@dataclass
class Pixel(BaseDataClass):
    """
    A class to store a pixel
    """

    coor: Coor = field(default_factory=Coor)
    color: Color = field(default_factory=Color)
    tolerance: int = field(default=20)
    region: str = field(default="root")

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'Pixel':
        return from_dict(data_class=cls, data=data)
