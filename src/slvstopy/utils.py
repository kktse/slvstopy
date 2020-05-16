from functools import reduce
from operator import getitem
from typing import List


def set_in_dict(data: dict, keys: List[str], val):
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = val
    return data


def get_in_dict(data: dict, *keys: str):
    for key in keys:
        try:
            data = data[key]
        except KeyError:
            return None

    return data
