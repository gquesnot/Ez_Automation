from app.components.my_input import MyInput
from app.components.my_select import MyStringEnumSelect
from baseclass.my_dataclass.tcr_scan_config import TcrScanConfig, TcrScanConfigs
from baseclass.my_enum.var_type import VarType
from app.view.base_view import BaseViewWithSelect


class TcrScansView(BaseViewWithSelect):
    datas: TcrScanConfigs = None
    baseClass: TcrScanConfig = TcrScanConfig
    selected: TcrScanConfig = None

    def __init__(self, app: 'App'):
        super().__init__(app, "tcrScans", app.game.config.tcrScans)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(
            MyStringEnumSelect(self, "Type", enum=VarType, value=data.type, row=self.rowStart + 1, path="data.type"))
        self.inputs.append(MyInput(self, "Region", data.region, row=self.rowStart + 2, path="data.region"))
        self.inputs.append(MyInput(self, "X", data.rectangle.x, row=self.rowStart + 3, path="data.rectangle.x"))
        self.inputs.append(MyInput(self, "Y", data.rectangle.y, row=self.rowStart + 4, path="data.rectangle.y"))
        self.inputs.append(MyInput(self, "w", data.rectangle.w, row=self.rowStart + 5, path="data.rectangle.w"))
        self.inputs.append(MyInput(self, "h", data.rectangle.h, row=self.rowStart + 6, path="data.rectangle.h"))
        self.rowStart += 7
        self.addBtnByHint(['save', 'delete', 'rectangle', 'test'])
