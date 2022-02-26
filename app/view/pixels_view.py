from app.components.my_input import MyInput
from app.components.my_select import MyStringEnumSelect
from baseclass.my_dataclass.pixel_config import PixelConfig, PixelConfigs
from baseclass.my_dataclass.pixel import Pixel
from baseclass.my_enum.condition_type import PixelConfigType
from app.view.base_view import BaseViewSelectWithChild


class PixelsView(BaseViewSelectWithChild):
    baseClass = PixelConfig
    childClassListName = "pixels"
    childClass: Pixel = Pixel
    datas: PixelConfigs = None

    def __init__(self, app: 'App'):
        super().__init__(app, "pixels", app.game.config.pixels)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(
            MyStringEnumSelect(self, "Type", enum=PixelConfigType, value=data.type, row=self.rowStart + 1,
                               path="data.type"))
        self.initChildSelect(datas=data.pixels, row=self.rowStart + 2)

        idx = self.childSelect.get()
        self.inputs.append(MyInput(self, label="Region", value=data.pixels[idx].region, row=self.rowStart + 3,
                                   path=f"data.pixels[{idx}].region"))
        self.inputs.append(MyInput(self, label="Tolerance", value=data.pixels[idx].tolerance, row=self.rowStart + 4,
                                   path=f"data.pixels[{idx}].tolerance"))
        self.inputs.append(MyInput(self, label="X", value=data.pixels[idx].coor.x, row=self.rowStart + 5,
                                   path=f"data.pixels[{idx}].coor.x"))
        self.inputs.append(MyInput(self, label="Y", value=data.pixels[idx].coor.y, row=self.rowStart + 6,
                                   path=f"data.pixels[{idx}].coor.y"))
        self.inputs.append(MyInput(self, label="R", value=data.pixels[idx].color.r, row=self.rowStart + 7,
                                   path=f"data.pixels[{idx}].color.r"))
        self.inputs.append(MyInput(self, label="G", value=data.pixels[idx].color.g, row=self.rowStart + 8,
                                   path=f"data.pixels[{idx}].color.g"))
        self.inputs.append(MyInput(self, label="B", value=data.pixels[idx].color.b, row=self.rowStart + 9,
                                   path=f"data.pixels[{idx}].color.b"))
        self.rowStart += 10
        self.addBtnByHint(["save", "delete", "pixel", "test"])
