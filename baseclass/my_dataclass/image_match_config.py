from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List

from dacite import from_dict, Config

from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from baseclass.my_enum.condition_type import ConditionType
from util.json_function import to_json


@dataclass
class ImageMatchItemConfig(BaseDataClass):
    """
    A class to store an image match item.
    """

    path: str = field(default="")
    region: str = field(default="root")
    img: Any = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ImageMatchItemConfig':
        return from_dict(data_class=cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        self.img = None
        return asdict(self)


@dataclass
class ImageMatchConfig(BaseDataClass):
    """
    A class to store an image match.
    """
    name: str = field(default="")
    type: ConditionType = field(default=ConditionType.OR)
    images: List[ImageMatchItemConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ImageMatchConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class ImageMatchConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of image match.
    """

    dict: Dict[str, ImageMatchConfig] = field(default_factory=dict)

    def save(self):
        to_json("imageMatch", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageMatchConfigs':
        return from_dict(data_class=cls, data=data, config=Config(cast=[ConditionType]))
