from os import system


def get_menus(title, menus):
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


def apply_type_of_var(string, value, type_of_var=None):
    if type_of_var is None:
        return type(value)(string)
    else:
        return type_of_var(string)


def ask_question(question, actual_var, type_of_var=None, clear_=False):
    if clear_:
        clear()
    res = -1
    while res == -1:
        value = input(f"\n{question}: {actual_var} => ")
        if value == "":
            return actual_var
        try:
            value = apply_type_of_var(value, actual_var, type_of_var)
            return value
        except:
            print("\nPlease enter a valid value")


def clear():
    system('cls')


def update_value_of_key(obj: dict, key, type_of_var=None):
    if key in obj:
        obj[key] = ask_question(f"{key}", obj[key], type_of_var)
    return obj


def get_menus_elements(obj: dict = None, names=None):
    if names is None:
        names = []
    res = []
    if obj is not None:
        for k, v in obj.items():
            res.append({'name': k, 'value': v})

    for idx, _ in enumerate(names):
        res.append({"name": _})
    return res
