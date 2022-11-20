from app.components.my_input import MyInput
from app.components.my_select import MyStringEnumSelect
from app.view.base_view import BaseViewSelectWithChild
from baseclass.my_dataclass.pixel import Pixel
from baseclass.my_dataclass.pixel_config import PixelConfig, PixelConfigs
from baseclass.my_enum.condition_type import ConditionType


class PixelsView(BaseViewSelectWithChild):
    base_class = PixelConfig
    child_class_list_name = "pixels"
    child_class: Pixel = Pixel
    datas: PixelConfigs = None

    def __init__(self, app: 'App'):
        super().__init__(app, "pixels", app.game.config.pixels)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.row_start, path="data.name"))
        self.inputs.append(
            MyStringEnumSelect(self, "Type", enum=ConditionType, value=data.type, row=self.row_start + 1,
                               path="data.type"))
        self.init_child_select(datas=data.pixels, row=self.row_start + 2)

        idx = self.child_select.get()
        self.inputs.append(MyInput(self, label="Region", value=data.pixels[idx].region, row=self.row_start + 3,
                                   path=f"data.pixels[{idx}].region"))
        self.inputs.append(MyInput(self, label="Tolerance", value=data.pixels[idx].tolerance, row=self.row_start + 4,
                                   path=f"data.pixels[{idx}].tolerance"))
        self.inputs.append(MyInput(self, label="X", value=data.pixels[idx].coor.x, row=self.row_start + 5,
                                   path=f"data.pixels[{idx}].coor.x"))
        self.inputs.append(MyInput(self, label="Y", value=data.pixels[idx].coor.y, row=self.row_start + 6,
                                   path=f"data.pixels[{idx}].coor.y"))
        self.inputs.append(MyInput(self, label="R", value=data.pixels[idx].color.r, row=self.row_start + 7,
                                   path=f"data.pixels[{idx}].color.r"))
        self.inputs.append(MyInput(self, label="G", value=data.pixels[idx].color.g, row=self.row_start + 8,
                                   path=f"data.pixels[{idx}].color.g"))
        self.inputs.append(MyInput(self, label="B", value=data.pixels[idx].color.b, row=self.row_start + 9,
                                   path=f"data.pixels[{idx}].color.b"))
        self.row_start += 10
        self.add_btn_by_hint(["save", "delete", "pixel", "test"])
