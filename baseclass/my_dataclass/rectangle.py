from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.coor import Coor


@dataclass
class Rectangle(Coor):
    """
    A class to store a rectangle.
    """

    w: int = field(default=0)
    h: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'Rectangle':
        return from_dict(data_class=cls, data=data)
