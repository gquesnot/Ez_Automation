from dataclasses import dataclass
from typing import List, Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass


@dataclass
class Color(BaseDataClass):
    """
    A class to store a color.
    """

    r: int = 0
    g: int = 0
    b: int = 0

    def asList(self) -> List[int]:
        return [self.r, self.g, self.b]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'Color':
        return from_dict(data_class=cls, data=data)
