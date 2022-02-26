from baseclass.my_dataclass.mask_detection_config import MaskDetectionConfig, MaskDetectionConfigs
from app.view.base_view import EzView


class MaskDetectionsView(EzView):
    childClass: MaskDetectionConfig = MaskDetectionConfig
    baseClass: MaskDetectionConfig = MaskDetectionConfig
    datas: MaskDetectionConfigs = None
    childClassListName = "images"
    hints = ["save", "delete", "mask", "test"]

    def __init__(self, app: 'App'):
        super().__init__(app, name="maskDetections", datas=app.game.config.maskDetections)
