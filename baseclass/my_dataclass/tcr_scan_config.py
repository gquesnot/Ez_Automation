from dataclasses import dataclass, field
from typing import Dict, Any

from dacite import from_dict, Config

from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from baseclass.my_dataclass.rectangle import Rectangle
from baseclass.my_enum.var_type import VarType
from util.json_function import toJson


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
