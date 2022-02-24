from controllers.configcontroller import ConfigController
from util.InputHandler import getMenusElements, getMenus
from util.threadclass import ThreadClass


class MenuController(ThreadClass):
    game = None

    menu = None

    def run(self):

        self.root()

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.config = ConfigController(self.game)

    def root(self):
        while not self.stopped:
            menu = getMenus("Root Menu",
                            getMenusElements(obj={"Freeze": self.game.freeze, "ClickInfo": self.game.imSave.clickInfo}, names=["Start", "Config", "Exit"]))

            match menu:
                case "Start":
                    print('start')
                case "Config":
                    # self.config.show()
                    self.config.getMainMenu()
                    pass
                case "Freeze":
                    self.game.toggleFreeze()
                case "ClickInfo":
                    self.game.imSave.clickInfo = not self.game.imSave.clickInfo
                case "Exit":
                    self.game.stopped = True
                    self.stopped = True

