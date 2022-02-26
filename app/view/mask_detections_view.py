from app.components.my_input import MyInput
from app.my_dataclasses import MaskDetectionConfig, MaskDetectionConfigs
from app.view.base_view import BaseViewWithSelect, EzView


class MaskDetectionsView(EzView):
    childClass: MaskDetectionConfig = MaskDetectionConfig
    baseClass: MaskDetectionConfig = MaskDetectionConfig
    datas: MaskDetectionConfigs = None
    childClassListName = "images"
    hints = ["save", "delete", "mask", "test"]

    def __init__(self, app: 'App'):
        super().__init__(app, name="maskDetections", datas=app.game.config.maskDetections)
