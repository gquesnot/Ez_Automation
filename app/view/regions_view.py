from app.components.my_input import MyInput
from baseclass.my_dataclass.region_config import RegionConfig, RegionConfigs
from app.view.base_view import BaseViewWithSelect


class RegionsView(BaseViewWithSelect):
    datas: RegionConfigs = None
    baseClass: RegionConfig = RegionConfig
    withTest: bool = True

    def __init__(self, app: 'App'):
        super().__init__(app, "regions", app.game.config.regions)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(MyInput(self, label="Ratio", value=data.ratio, row=self.rowStart + 1, path="data.ratio"))

        self.inputs.append(
            MyInput(self, label="X", value=data.rectangle.x, row=self.rowStart + 2, path="data.rectangle.x"))
        self.inputs.append(
            MyInput(self, label="Y", value=data.rectangle.y, row=self.rowStart + 3, path="data.rectangle.y"))
        self.inputs.append(
            MyInput(self, label="W", value=data.rectangle.w, row=self.rowStart + 4, path="data.rectangle.w"))
        self.inputs.append(
            MyInput(self, label="H", value=data.rectangle.h, row=self.rowStart + 5, path="data.rectangle.h"))
        self.rowStart += 6
        self.addBtnByHint(["save", "delete", "rectangle", "test"])
