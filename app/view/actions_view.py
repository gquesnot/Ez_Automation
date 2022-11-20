from app.components.my_input import MyInput
from app.view.base_view import BaseViewWithSelect, EzView
from baseclass.my_dataclass.action_config import KeyboardActionConfig, MouseActionConfig, MouseActionConfigs
from baseclass.my_dataclass.action_record_config import ActionRecordConfigs, ActionRecordConfig


class MouseActionsView(BaseViewWithSelect):
    datas: MouseActionConfigs = None
    base_class: MouseActionConfig = MouseActionConfig
    with_test: bool = False

    def __init__(self, app: 'App'):
        super().__init__(app, "mouseActions", app.game.config.mouseActions)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.row_start, path="data.name"))
        self.inputs.append(MyInput(self, "Delay", data.delay, row=self.row_start + 1, path="data.delay"))
        self.inputs.append(
            MyInput(self, "Sleep After", data.sleep_after, row=self.row_start + 2, path="data.sleepAfter"))
        self.inputs.append(MyInput(self, "Region", data.region, row=self.row_start + 3, path="data.region"))
        self.inputs.append(MyInput(self, "X", data.coor.x, row=self.row_start + 4, path="data.coor.x"))
        self.inputs.append(MyInput(self, "Y", data.coor.y, row=self.row_start + 5, path="data.coor.y"))
        self.row_start += 6
        self.add_btn_by_hint(['save', 'delete', 'coor', 'test'])


class KeyboardActionsView(BaseViewWithSelect):
    datas: MouseActionConfig = None
    baseClass: KeyboardActionConfig = KeyboardActionConfig
    withTest: bool = False

    def __init__(self, app: 'App'):
        super().__init__(app, "keyboardActions", app.game.config.keyboardActions)
        data = self.parent_select.get_obj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.row_start, path="data.name"))
        self.inputs.append(MyInput(self, "Delay", data.delay, row=self.row_start + 1, path="data.delay"))
        self.inputs.append(
            MyInput(self, "Sleep After", data.sleep_after, row=self.row_start + 2, path="data.sleepAfter"))
        self.inputs.append(MyInput(self, "Key", data.key, row=self.row_start + 3, path="data.key"))
        self.row_start += 4
        self.add_btn_by_hint(['save', 'delete', 'test'])


class RecordPlayActionView(EzView):
    datas: ActionRecordConfigs = None
    base_class: ActionRecordConfig = ActionRecordConfig

    hints = ['save', 'new', 'delete', 'minify', 'record', 'replay']

    def __init__(self, app: 'App'):
        super().__init__(app, app.game.config.replayActions, "replayActions")
