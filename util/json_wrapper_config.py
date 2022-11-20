from dataclasses import dataclass, field
from typing import Any, Union, List, Dict

from dacite import from_dict

from util.wrapper_config import WrapperConfig


@dataclass
class JsonWrapperConfig(WrapperConfig):
    path: Union[str, List[str], None] = field(default=None)
    configIndex: Union[ConfigIndex, None] = field(default=None)
    url: Union[str, List[str]] = field(default=None)
    urlHint: str = field(default="")

    def set_json(self, datas):
        datas = withoutDataDict(datas)
        if self.url is not None and (isinstance(self.url, list) and len(self.url) > 1):
            if self.json is None:
                self.json = []
            self.json.append(datas)
        else:
            self.json = datas

    @classmethod
    def from_dict(cls, idx: int, data: Dict[str, Any]) -> "JsonWrapperConfig":
        data['id'] = idx
        if "path" not in data.keys():
            data['path'] = data['name']
        return from_dict(cls, data=data)
