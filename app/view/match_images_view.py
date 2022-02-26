from app.components.my_input import MyInput, MyImg
from baseclass.my_dataclass.image_match_config import ImageMatchItemConfig, ImageMatchConfig, ImageMatchConfigs
from app.view.base_view import BaseViewSelectWithChild


class MatchImagesView(BaseViewSelectWithChild):
    childClass: ImageMatchItemConfig = ImageMatchItemConfig
    baseClass: ImageMatchConfig = ImageMatchConfig
    datas: ImageMatchConfigs = None
    childClassListName = "images"

    def __init__(self, app: 'App'):
        super().__init__(app, "matchImages", app.game.config.matchImages)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.rowStart, path="data.name"))
        self.initChildSelect(datas=data.images, row=self.rowStart + 1)
        idx = self.childSelect.get()
        self.inputs.append(MyInput(self, label="Region", value=data.images[idx].region, row=self.rowStart + 2,
                                   path=f"data.images[{idx}].region"))
        self.inputs.append(MyInput(self, label="Path", value=data.images[idx].path, row=self.rowStart + 3,
                                   path=f"data.images[{idx}].path"))
        self.img = MyImg(self, imgPath=data.images[idx].path, row=self.rowStart + 4, col=1,
                         path=f"data.images[{idx}].image")
        self.rowStart += 5
        self.addBtnByHint(["save", "delete", "image", "test"])
