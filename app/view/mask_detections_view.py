from app.components.my_input import MyInput
from app.view.base_view import BaseViewWithSelect
from baseclass.my_dataclass.mask_detection_config import MaskDetectionConfig, MaskDetectionConfigs


class MaskDetectionsView(BaseViewWithSelect):
    base_class: MaskDetectionConfig = MaskDetectionConfig
    datas: MaskDetectionConfigs = None
    with_test: bool = True

    def __init__(self, app: 'App'):
        super().__init__(app, name="mask_detections", datas=app.game.config.mask_detections)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.row_start, path="data.name"))
        self.inputs.append(MyInput(self, label="Region", value=data.region, row=self.row_start + 1, path="data.region"))
        self.inputs.append(
            MyInput(self, label="Min area", value=data.min_area, row=self.row_start + 2, path="data.minArea"))
        self.inputs.append(
            MyInput(self, label="Max found", value=data.max_found, row=self.row_start + 3, path="data.maxFound"))

        self.inputs.append(
            MyInput(self, label="Lower R", value=data.lower.r, row=self.row_start + 4, path="data.lower.r"))
        self.inputs.append(
            MyInput(self, label="Lower G", value=data.lower.g, row=self.row_start + 5, path="data.lower.g"))
        self.inputs.append(
            MyInput(self, label="Lower B", value=data.lower.b, row=self.row_start + 6, path="data.lower.b"))
        self.inputs.append(
            MyInput(self, label="Upper R", value=data.upper.r, row=self.row_start + 7, path="data.upper.r"))
        self.inputs.append(
            MyInput(self, label="Upper G", value=data.upper.g, row=self.row_start + 8, path="data.upper.g"))
        self.inputs.append(
            MyInput(self, label="Upper B", value=data.upper.b, row=self.row_start + 9, path="data.upper.b"))
        self.row_start += 10
        self.add_btn_by_hint(["save", "delete", "mask", 'test mask'])
