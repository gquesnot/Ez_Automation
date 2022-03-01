from dataclasses import dataclass, field
from typing import List, Dict, Any

from dacite import from_dict

from baseclass.my_dataclass.base_dataclass import BaseDataClass


@dataclass
class Coor(BaseDataClass):
    """
    A class to store coordinates.
    """
    x: int = field(default=0)
    y: int = field(default=0)

    def hasList(self) -> List[int]:
        return [self.x, self.y]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'Coor':
        return from_dict(data_class=cls, data=data)
