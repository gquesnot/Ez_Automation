from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass


@dataclass
class WindowConfig(BaseDataClass):
    """
    A class to store a window.
    """

    name: str = field(default="")
    cropped_y: int = field(default=0)
    h_diff: int = field(default=0)
    cropped_x: int = field(default=0)
    w_diff: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'WindowConfig':
        return from_dict(data_class=cls, data=data)
