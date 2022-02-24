from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field, fields
from enum import Enum
from typing import Any, Dict, Union, List

from dacite import from_dict, Config

from util.json_function import toJson


class PixelConfigType(str, Enum):
    AND = "AND"
    OR = "OR"


class VarType(str, Enum):
    INT = "INT"
    STRING = "STRING"


class ActionType(str, Enum):
    Keyboard = "Keyboard"
    MouseMove = "MouseMove"
    MouseClick = "MouseClick"
    MouseMoveClick = "MouseMoveClick"


@dataclass
class GetSetDict(ABC):
    """
    Abstract class for all dataclasses that need to be converted to dicts
    """
    dict: Dict[str, Any] = field(default_factory=dict)




    def get(self, name: str) -> Any:
        if name in self.dict:
            return self.dict[name]
        return None

    def updateName(self, oldName, newName: str) -> None:
        self.dict[newName] = self.dict.pop(oldName)

    def set(self, action: Any) -> None:
        self.dict[action.name] = action

    def remove(self, name: str) -> None:
        del self.dict[name]

    def clear(self) -> None:
        self.dict.clear()

    def isEmpty(self) -> bool:
        return len(self.dict) == 0

    def update(self, other: Any) -> None:
        self.dict.update(other.dict)

    def fromIdx(self, idx: int) -> Any:
        return self.dict[self.keyAsList()[idx]]

    def getIdx(self, name: str) -> int:
        return self.keyAsList().index(name)

    def keyAsList(self) -> list:
        return list(self.dict)

    @abstractmethod
    def save(self):
        pass


@dataclass
class BaseDataClass(ABC):
    """
    Base class for all data classes.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        return from_dict(data_class=cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the data class to a dictionary.
        :return: A dictionary representation of the data class.
        """
        return asdict(self)

    def apply(self, obj):
        """
        apply the data class to an object
        :param obj: the object to apply the data class to

        :param obj:
        :return:
        """
        for attr in fields(self):
            value = getattr(self, attr.name)
            setattr(obj, attr.name, value)


@dataclass
class Coor(BaseDataClass):
    """
    A class to store coordinates.
    """
    x: int = field(default=0)
    y: int = field(default=0)

    def hasList(self) -> List[int]:
        return [self.x, self.y]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'Coor':
        return from_dict(data_class=cls, data=data)


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
        toJson("region", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'RegionConfigs':
        return from_dict(data_class=cls, data=data)


@dataclass
class ImageMatchItemConfig(BaseDataClass):
    """
    A class to store an image match item.
    """

    path: str = field(default="")
    region: str = field(default="root")
    image: Any = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ImageMatchItemConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class ImageMatchConfig(BaseDataClass):
    """
    A class to store an image match.
    """
    name: str = field(default="")
    images: List[ImageMatchItemConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'ImageMatchConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class Pixel(BaseDataClass):
    """
    A class to store a pixel.
    """

    coor: Coor = field(default_factory=Coor)
    color: Color = field(default_factory=Color)
    tolerance: int = field(default=0)
    region: str = field(default="root")

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'Pixel':
        return from_dict(data_class=cls, data=data)


@dataclass
class PixelConfig(BaseDataClass):
    """
    A class to store a pixel List with relation.
    """
    name: str = field(default="")
    type: PixelConfigType = field(default="OR")
    pixels: List[Pixel] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'PixelConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class TcrScanConfig(BaseDataClass):
    """
    A class to store a TCR Scan.
    """

    name: str = field(default="")
    region: str = field(default="root")
    rectangle: Rectangle = field(default_factory=Rectangle)
    type: VarType = field(default=VarType.STRING)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> 'TcrScanConfig':
        return from_dict(data_class=cls, data=data)


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


@dataclass
class ActionBaseConfig(BaseDataClass, ABC):
    """
    A class to store an action.
    """
    name: str = field(default="")
    delay: float = field(default=.1)
    sleepAfter: float = field(default=.1)
    type: ActionType = field(default=ActionType.Keyboard)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionBaseConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class KeyBoardActionConfig(ActionBaseConfig):
    """
    A class to store a keyboard action.
    """

    key: str = field(default='')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyBoardActionConfig':
        return from_dict(data_class=cls, data=data, config=Config(cast=[ActionType]))


@dataclass
class MouseActionConfig(ActionBaseConfig):
    """
    A class to store a mouse action.
    """

    coor: Coor = field(default=Coor)
    region: str = field(default="root")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MouseActionConfig':
        return from_dict(data_class=cls, data=data, config=Config(cast=[ActionType]))


@dataclass
class ActionConfig(BaseDataClass):
    """
    A class to store an action.
    """

    type: ActionType = field(default=ActionType.Keyboard)
    keyboard: KeyBoardActionConfig = field(default=KeyBoardActionConfig())
    mouse: MouseActionConfig = field(default=MouseActionConfig())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionConfig':
        return from_dict(data_class=cls, data=data)


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


@dataclass
class ActionConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of actions.
    """

    dict: Dict[str, Union[MouseActionConfig, KeyBoardActionConfig]] = field(default_factory=dict)

    def save(self):
        toJson("action", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionConfigs':
        res = {}
        for k, v in data['dict'].items():
            if "Mouse" in v['type']:
                res[k] = MouseActionConfig.from_dict(v)
            else:
                res[k] = KeyBoardActionConfig.from_dict(v)
        return cls(dict=res)


@dataclass
class TcrScanConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of TCR Scan.
    """

    dict: Dict[str, TcrScanConfig] = field(default_factory=dict)

    def save(self):
        toJson("tcrScan", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TcrScanConfigs':
        return from_dict(data_class=cls, data=data, config=Config(cast=[VarType]))


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
        return from_dict(data_class=cls, data=data, config=Config(cast=[PixelConfigType]))


@dataclass
class ImageMatchConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a list of image match.
    """

    dict: Dict[str, ImageMatchConfig] = field(default_factory=dict)

    def save(self):
        toJson("imageMatch", self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageMatchConfigs':
        return from_dict(data_class=cls, data=data)
