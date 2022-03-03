from app.components.my_input import MyInput
from app.view.base_view import BaseViewWithSelect, EzView
from baseclass.my_dataclass.action_config import KeyboardActionConfig, MouseActionConfig, MouseActionConfigs, \
    KeyboardActionConfigs
from baseclass.my_dataclass.action_record_config import ActionRecordConfigs, ActionRecordConfig


class MouseActionsView(BaseViewWithSelect):
    datas: MouseActionConfigs = None
    baseClass: MouseActionConfig = MouseActionConfig
    withTest: bool = False

    def __init__(self, app: 'App'):
        super().__init__(app, "mouseActions", app.game.config.mouseActions)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(MyInput(self, "Delay", data.delay, row=self.rowStart + 1, path="data.delay"))
        self.inputs.append(MyInput(self, "Sleep After", data.sleepAfter, row=self.rowStart + 2, path="data.sleepAfter"))
        self.inputs.append(MyInput(self, "Region", data.region, row=self.rowStart + 3, path="data.region"))
        self.inputs.append(MyInput(self, "X", data.coor.x, row=self.rowStart + 4, path="data.coor.x"))
        self.inputs.append(MyInput(self, "Y", data.coor.y, row=self.rowStart + 5, path="data.coor.y"))
        self.rowStart += 6
        self.addBtnByHint(['save', 'delete', 'coor', 'test'])


class KeyboardActionsView(BaseViewWithSelect):
    datas: MouseActionConfig = None
    baseClass: KeyboardActionConfig = KeyboardActionConfig
    withTest: bool = False

    def __init__(self, app: 'App'):
        super().__init__(app, "keyboardActions", app.game.config.keyboardActions)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(MyInput(self, "Delay", data.delay, row=self.rowStart + 1, path="data.delay"))
        self.inputs.append(MyInput(self, "Sleep After", data.sleepAfter, row=self.rowStart + 2, path="data.sleepAfter"))
        self.inputs.append(MyInput(self, "Key", data.key, row=self.rowStart + 3, path="data.key"))
        self.rowStart += 4
        self.addBtnByHint(['save', 'delete', 'test'])


class RecordPlayActionView(EzView):
    datas:ActionRecordConfigs  = None
    baseClass: ActionRecordConfig = ActionRecordConfig

    hints = ['save', 'new', 'delete', 'minify','record', 'replay']

    def __init__(self, app: 'App'):
        super().__init__(app, app.game.config.replayActions, "replayActions")
