from os import system


def getMenus(title, menus, clear_=True):
    res = -1
    while res == -1:
        # if clear_:
        #     clear()
        print("\n" + title)
        for i, menu in enumerate(menus):
            row = str(i + 1) + " - " + menu['name']
            if 'value' in menu:
                row += " => " + str(menu['value'])
            print(row)
        value = input("\nChoose an option: ")
        if (value == "") or (value == "0"):
            return ""
        try:
            value = int(value)
            if 0 < value <= len(menus):
                return menus[value - 1]['name']
        except:
            print("\nPlease enter a valid option")



def applyTypeOfVar(string, value, typeOfVar=None):
    if typeOfVar is None:
        return type(value)(string)
    else:
        return typeOfVar(string)


def askQuestion(question, actualVar, typeOfVar=None, clear_=False):
    if clear_:
        clear()
    res = -1
    while res == -1:
        value = input(f"\n{question}: {actualVar} => ")
        if value == "":
            return actualVar
        try:
            value = applyTypeOfVar(value, actualVar, typeOfVar)
            return value
        except:
            print("\nPlease enter a valid value")


def clear():
    system('cls')


def updateValueOfKey(obj: dict, key, typeOfVar=None):
    if key in obj:
        obj[key] = askQuestion(f"{key}", obj[key], typeOfVar)
    return obj


def getMenusElements(obj: dict = None, names=None):
    if names is None:
        names = []
    res = []
    if obj is not None:
        for k, v in obj.items():
            res.append({'name': k, 'value': v})

    for idx, _ in enumerate(names):
        res.append({"name": _})
    return res
