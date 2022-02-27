from app.components.my_input import MyInput
from baseclass.my_dataclass.mask_detection_config import MaskDetectionConfig, MaskDetectionConfigs
from app.view.base_view import EzView, BaseViewWithSelect


class MaskDetectionsView(BaseViewWithSelect):
    baseClass: MaskDetectionConfig = MaskDetectionConfig
    datas: MaskDetectionConfigs = None
    withTest: bool = True

    def __init__(self, app: 'App'):
        super().__init__(app, name="maskDetections", datas=app.game.config.maskDetections)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(MyInput(self, label="Region", value=data.region, row=self.rowStart+1, path="data.region"))
        self.inputs.append(MyInput(self, label="Min area", value=data.minArea, row=self.rowStart+2, path="data.minArea"))
        self.inputs.append(MyInput(self, label="Max found", value=data.maxFound, row=self.rowStart+3, path="data.maxFound"))

        self.inputs.append(MyInput(self, label="Lower R", value=data.lower.r, row=self.rowStart+4, path="data.lower.r"))
        self.inputs.append(MyInput(self, label="Lower G", value=data.lower.g, row=self.rowStart+5, path="data.lower.g"))
        self.inputs.append(MyInput(self, label="Lower B", value=data.lower.b, row=self.rowStart+6, path="data.lower.b"))
        self.inputs.append(MyInput(self, label="Upper R", value=data.upper.r, row=self.rowStart+7, path="data.upper.r"))
        self.inputs.append(MyInput(self, label="Upper G", value=data.upper.g, row=self.rowStart+8, path="data.upper.g"))
        self.inputs.append(MyInput(self, label="Upper B", value=data.upper.b, row=self.rowStart+9, path="data.upper.b"))
        self.rowStart += 10
        self.addBtnByHint(["save", "delete", "mask", 'test mask'])
