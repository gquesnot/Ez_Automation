from dataclasses import dataclass, field
from typing import Dict, Any, Union, List

from dacite import from_dict

from baseclass.my_dataclass.action_record import ActionKeyBoardRecord, ActionMouseClickRecord, \
    ActionMouseDragRecord
from baseclass.my_dataclass.base_dataclass import BaseDataClass, GetSetDict
from util.json_function import to_json


@dataclass
class ActionRecordConfig(BaseDataClass):
    """
    A class to store a mask detection.
    """

    name: str = field(default="")
    keys: List[ActionKeyBoardRecord] = field(default_factory=list)
    clicks: List[Union[ActionMouseClickRecord, ActionMouseDragRecord]] = field(default_factory=list)

    def total_duration(self):
        max_key = max(self.keys, key=lambda x: x.end_at).end_at if len(self.keys) > 0 else 0
        max_click = max(self.clicks, key=lambda x: x.endAt).end_at if len(self.clicks) > 0 else 0
        print(max_click, max_key)
        return max(max_key, max_click)

    def all(self):
        new_list = [*self.keys, *self.clicks]
        new_list.sort(key=lambda x: x.start_at)
        return new_list

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRecordConfig':
        return from_dict(data_class=cls, data=data)


@dataclass
class ActionRecordConfigs(BaseDataClass, GetSetDict):
    """
    A class to store a dict of action records.
    """

    def save(self):
        to_json("replayActions.json", self.to_dict())

    dict: Dict[str, ActionRecordConfig] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRecordConfigs':
        return from_dict(data_class=cls, data=data)
