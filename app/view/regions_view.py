from app.components.my_input import MyInput
from app.view.base_view import BaseViewWithSelect
from baseclass.my_dataclass.region_config import RegionConfig, RegionConfigs


class RegionsView(BaseViewWithSelect):
    datas: RegionConfigs = None
    base_class: RegionConfig = RegionConfig
    with_test: bool = True

    def __init__(self, app: 'App'):
        super().__init__(app, "regions", app.game.config.regions)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.row_start, path="data.name"))
        self.inputs.append(MyInput(self, label="Ratio", value=data.ratio, row=self.row_start + 1, path="data.ratio"))

        self.inputs.append(
            MyInput(self, label="X", value=data.rectangle.x, row=self.row_start + 2, path="data.rectangle.x"))
        self.inputs.append(
            MyInput(self, label="Y", value=data.rectangle.y, row=self.row_start + 3, path="data.rectangle.y"))
        self.inputs.append(
            MyInput(self, label="W", value=data.rectangle.w, row=self.row_start + 4, path="data.rectangle.w"))
        self.inputs.append(
            MyInput(self, label="H", value=data.rectangle.h, row=self.row_start + 5, path="data.rectangle.h"))
        self.row_start += 6
        self.add_btn_by_hint(["save", "delete", "rectangle"])
