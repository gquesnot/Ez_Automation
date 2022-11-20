import re


def map_data_class_fields(dc, data, to_map):
    for k, v in to_map.items():
        my_data = data[k]
        if v['list']:
            if isinstance(my_data, dict):
                my_data = [val | {"id": key} for key, val in my_data.items()]

            my_data = [map_field(dc, v['type']) for val in my_data]
        else:
            my_data = map_field(dc, v['type'])
        data[k] = my_data

    return data


def map_field(dc, class_):
    return class_.from_dict(dc, ).to_dict()


def own_capitalize(string):
    return re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), string, 1)


def str_to_float_list(string, separator="/"):
    return [float(v) for v in string.split(separator)]
