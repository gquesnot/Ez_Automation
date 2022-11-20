class RectangleCoor:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.x1 = self.x + self.w
        self.y1 = self.y + self.h
        self.center_x = self.x + int(self.w / 2)
        self.center_y = self.y + int(self.h / 2)

    def get_diff(self, other):
        return abs(self.center_x - other.centerX) + abs(self.center_y - other.centerY)

    def get_coor(self, hint=""):
        if hint == "":
            return self.x, self.y, self.w, self.h
        elif hint == "dict":
            return {"x": self.x,
                    "y": self.y,
                    "w": self.w,
                    "h": self.h
                    }
        elif hint == "xyx1y1":
            return self.x, self.y, self.x1, self.y1
        elif hint == "center":
            return self.center_x, self.center_y

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, x1: {self.x1}, y1: {self.y1}, w:{self.w}, h: {self.h}, centerX: {self.centerX}, centerY: {self.centerY}"

    def __eq__(self, other):
        return self.get_diff(other) <= 20

    def update(self):
        self.x1 = self.x + self.w
        self.y1 = self.y + self.h
        self.center_x = self.x + int(self.w / 2)
        self.center_y = self.y + int(self.h / 2)
