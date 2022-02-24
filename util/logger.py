class Logger:
    H1 = "-----   {}   -----\n"
    H2 = "---  {}  ---\n"
    H3 = "-- {} --\n"

    def __init__(self):
        self.str = ""

    def reset(self):
        self.str = ""

    def addFromLog(self, lg, lvl=0):
        res = lg.split('\n')
        for idx, elem in enumerate(res):
            res[idx] = self.getALvl(lvl) + elem
        self.str += "\n".join(res)

    def getALvl(self, lvl):
        tmp = ""
        for i in range(lvl):
            tmp += "	"
        return tmp

    def newLine(self, nb=1):
        for i in range(0, nb):
            self.str += "\n"

    def addLvl(self, lvl=0):
        for i in range(0, lvl):
            self.str += "	"

    def addLine(self, line, lvl=0):
        self.addLvl(lvl)
        self.str += line + "\n"

    def addArrayAsLine(self, array, sperator=",", lvl=0):
        res = ""
        for idx, elem in enumerate(array):
            if idx < len(array) - 1:
                res += elem + sperator + " "
            else:
                res += elem
        self.addLine(res, lvl)

    def addTitle(self, title, titleLvl="-- {} --\n", lvl=0):
        if titleLvl == self.H1:
            self.str += "\n\n"
        else:
            self.str += "\n"
        self.addLvl(lvl)
        self.str += titleLvl.format(title.upper())

    def __str__(self):
        return self.str
