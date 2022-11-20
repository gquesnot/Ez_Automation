from app.components.my_input import MyInput
from app.components.my_select import MyStringEnumSelect
from app.view.base_view import BaseViewWithSelect
from baseclass.my_dataclass.tcr_scan_config import TcrScanConfig, TcrScanConfigs
from baseclass.my_enum.var_type import VarType


class TcrScansView(BaseViewWithSelect):
    datas: TcrScanConfigs = None
    base_class: TcrScanConfig = TcrScanConfig
    selected: TcrScanConfig = None

    def __init__(self, app: 'App'):
        super().__init__(app, "tcrScans", app.game.config.tcrScans)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.row_start, path="data.name"))
        self.inputs.append(
            MyStringEnumSelect(self, "Type", enum=VarType, value=data.type, row=self.row_start + 1, path="data.type"))
        self.inputs.append(MyInput(self, "Region", data.region, row=self.row_start + 2, path="data.region"))
        self.inputs.append(MyInput(self, "X", data.rectangle.x, row=self.row_start + 3, path="data.rectangle.x"))
        self.inputs.append(MyInput(self, "Y", data.rectangle.y, row=self.row_start + 4, path="data.rectangle.y"))
        self.inputs.append(MyInput(self, "w", data.rectangle.w, row=self.row_start + 5, path="data.rectangle.w"))
        self.inputs.append(MyInput(self, "h", data.rectangle.h, row=self.row_start + 6, path="data.rectangle.h"))
        self.row_start += 7
        self.add_btn_by_hint(['save', 'delete', 'rectangle', 'test'])
