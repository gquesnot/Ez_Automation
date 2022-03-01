from dataclasses import dataclass, field
from typing import Dict, Any, Union, List

from dacite import from_dict

from baseclass.my_dataclass.action_record import ActionKeyBoardRecord, ActionMouseClickRecord, \
    ActionMouseDragRecord
from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from util.json_function import toJson


@dataclass
class ActionRecordConfig(BaseDataClass):
    """
    A class to store a mask detection.
    """

    name: str = field(default="")
    actions: List[Union[ActionKeyBoardRecord, ActionMouseClickRecord, ActionMouseDragRecord]] = field(default_factory=list)

    def totalDuration(self):
        return max(self.actions, key=lambda x: x.endAt).endAt

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRecordConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class ActionRecordConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a dict of action records.
    """

    def save(self):
        toJson("replayActions.json", self.to_dict())

    dict: Dict[str, ActionRecordConfig] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRecordConfigs':
        return from_dict(data_class=cls, data=data)
