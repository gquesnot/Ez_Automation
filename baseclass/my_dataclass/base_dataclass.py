from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict, fields
from typing import Dict, Any

from dacite import from_dict


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

    def set(self, action: Any, oldName=None) -> None:
        if oldName is not None:
            del self.dict[oldName]
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
