from app.components.my_input import MyInput, MyImg
from app.view.base_view import BaseViewSelectWithChild
from baseclass.my_dataclass.image_match_config import ImageMatchItemConfig, ImageMatchConfig, ImageMatchConfigs


class MatchImagesView(BaseViewSelectWithChild):
    child_class: ImageMatchItemConfig = ImageMatchItemConfig
    base_class: ImageMatchConfig = ImageMatchConfig
    datas: ImageMatchConfigs = None
    child_class_list_name = "images"

    def __init__(self, app: 'App'):
        super().__init__(app, "matchImages", app.game.config.matchImages)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.row_start, path="data.name"))
        self.init_child_select(datas=data.images, row=self.row_start + 1)
        idx = self.child_select.get()
        print(idx)
        self.inputs.append(MyInput(self, label="Region", value=data.images[idx].region, row=self.row_start + 2,
                                   path=f"data.images[{idx}].region"))
        self.inputs.append(MyInput(self, label="Path", value=data.images[idx].path, row=self.row_start + 3,
                                   path=f"data.images[{idx}].path"))
        self.img = MyImg(self, imgPath=data.images[idx].path, row=self.row_start + 4, col=1,
                         path=f"data.images[{idx}].image")
        self.row_start += 5
        self.add_btn_by_hint(["save", "delete", "image", "test"])
