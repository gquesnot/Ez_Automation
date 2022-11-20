import json
import os

import requests


def get_value(obj, key):
    if isinstance(obj, dict):
        return obj[key]
    else:
        return getattr(obj, key)


def list_match_list(ll1, ll2):
    if not len(ll1):
        return True
    for l1 in ll1:
        if l1 in ll2:
            return True
    return False


def get_json(name, directory="json_data/"):
    files = os.listdir(directory)
    for file in files:
        if name + ".json" in file:
            with open(os.path.join(directory, file)) as jsonFile:
                data = json.load(jsonFile)
            return data
    return []


def save_json_api_response_in_json_file(url, file_path):
    with open(file_path, "w+") as f:
        r_json = requests.get(url).json()
        json.dump(r_json, f, indent=4)
        return r_json


def apply_json_config(obj, name, directory="json_data/"):
    res = []
    for k, v in get_json(name, directory=directory).items():
        setattr(obj, k, v)
        res.append(k)
    return res


def to_json(name, data, directory="json_data/"):
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(data, f, indent=2)


def append_json(name, data, directory=""):
    datastore = get_json(directory, name)
    if name == "verifiedLol":
        del data['birthdate']
        del data['confirm_password']
        mail = data['email'][0] + "@" + data['email'][1]
        data['email'] = mail

    datastore.append(data)
    directory = "json/" + directory
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(datastore, f, indent=2)


def json_print(data_name, data):
    print(data_name + ":", json.dumps(data, indent=2))
