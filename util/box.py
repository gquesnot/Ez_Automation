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

    def has_champ(self):
        if self.champ is None:
            return False
        else:
            return True

    def get_champ(self):
        return self.champ

    def get_id(self):
        return self.id

    def get_coor(self):
        return self.coor

    def get_champ_value(self):
        return self.champ.getValue() if self.has_champ() else 0

    def get_pos_as_coor(self):
        if self.type == "game":
            return math.floor(self.id / 7), self.id % 7
        else:
            return self.id

    def get_coor_has_tuple(self):
        return self.coor['x'], self.coor['y']

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def __str__(self):
        res = "{} Name: {}, ".format(self.type, self.get_name())
        if self.has_champ():
            res += str(self.champ)
        else:
            res += "hasChamp: False"
        return res
