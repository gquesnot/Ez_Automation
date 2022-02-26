import math


class Box:
    def __init__(self, game, id_, coor, type_, champ=None):
        self.game = game
        self.type = type_
        self.coor = coor
        self.name = "{}_{}".format(type_, str(id_))
        self.champ = champ
        self.id = id_

    def reset(self):
        self.champ = None

    def hasChamp(self):
        if self.champ is None:
            return False
        else:
            return True

    def getChamp(self):
        return self.champ

    def getId(self):
        return self.id

    def getCoor(self):
        return self.coor

    def getChampValue(self):
        return self.champ.getValue() if self.hasChamp() else 0

    def getPosAsCoor(self):
        if self.type == "game":
            return math.floor(self.id / 7), self.id % 7
        else:
            return self.id

    def getCoorHasTuple(self):
        return self.coor['x'], self.coor['y']

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def __str__(self):
        res = "{} Name: {}, ".format(self.type, self.getName())
        if self.hasChamp():
            res += str(self.champ)
        else:
            res += "hasChamp: False"
        return res
