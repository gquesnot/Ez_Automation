import re


def mapDataClassFields(dc, data, toMap):
    for k, v in toMap.items():
        myData = data[k]
        if v['list']:
            if isinstance(myData, dict):
                myData = [val | {"id": key} for key, val in myData.items()]

            myData = [mapField(dc, v['type'], val) for val in myData]
        else:
            myData = mapField(dc, v['type'], myData)
        data[k] = myData

    return data


def mapField(dc, Class, data):
    return Class.from_dict(dc, ).to_dict()


def ownCapitalize(string):
    return re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), string, 1)


def strToFloatList(string, separator="/"):
    return [float(v) for v in string.split(separator)]
