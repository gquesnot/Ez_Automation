class Logger:
    h1 = "-----   {}   -----\n"
    h2 = "---  {}  ---\n"
    h3 = "-- {} --\n"

    def __init__(self):
        self.str = ""

    def reset(self):
        self.str = ""

    def add_from_log(self, lg, lvl=0):
        res = lg.split('\n')
        for idx, elem in enumerate(res):
            res[idx] = self.get_a_lvl(lvl) + elem
        self.str += "\n".join(res)

    def get_a_lvl(self, lvl):
        tmp = ""
        for i in range(lvl):
            tmp += "	"
        return tmp

    def new_line(self, nb=1):
        for i in range(0, nb):
            self.str += "\n"

    def add_lvl(self, lvl=0):
        for i in range(0, lvl):
            self.str += "	"

    def add_line(self, line, lvl=0):
        self.add_lvl(lvl)
        self.str += line + "\n"

    def add_array_as_line(self, array, sperator=",", lvl=0):
        res = ""
        for idx, elem in enumerate(array):
            if idx < len(array) - 1:
                res += elem + sperator + " "
            else:
                res += elem
        self.add_line(res, lvl)

    def add_title(self, title, title_lvl="-- {} --\n", lvl=0):
        if title_lvl == self.h1:
            self.str += "\n\n"
        else:
            self.str += "\n"
        self.add_lvl(lvl)
        self.str += title_lvl.format(title.upper())

    def __str__(self):
        return self.str
