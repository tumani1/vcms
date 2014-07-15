# coding: utf-8
import time


# Возвращает массив состоящий из значений всех полей key
# в двумерном массиве или в массиве объектов list
def list_of(list, key, objects=False, distinct=False):
    result_list = []
    for item in list:
        if objects:
            value = getattr(item, key)
        else:
            value = item[key]

        if distinct:
            if not value in result_list:
                result_list.append(value)
        else:
            result_list.append(value)

    return result_list


# Преобразует массив объектов, в масисв с ключем по полю key
def reindex_by(list, key, objects=False):
    result_dict = {}
    for item in list:
        if objects: k_value = getattr(item, key)
        else: k_value = item[key]
        result_dict[k_value] = item

    return result_dict


# Сгруппировать двумерный массив или массив объектов
# по полю с именем key
def group_by(list, key, objects=False):
    result_dict = {}
    for item in list:
        if objects: k_value = getattr(item, key)
        else: k_value = item[key]

        if not result_dict.has_key(k_value):
            result_dict[k_value] = []
        result_dict[k_value].append(item)

    return result_dict


# Возвращает OrderedDict уровень-ключь
def get_lvls_for_dict(item, lvls=None, lvl=0):
    if lvls is None:
        lvls = {}
    if lvl not in lvls:
        lvls[lvl] = set()
    if isinstance(item, dict):
        keys = item.keys()
        lvls[lvl] |= set(keys)
        for key in keys:
            if isinstance(item[key], dict):
                get_lvls_for_dict(item[key], lvls, lvl+1)
    else:
        lvls[lvl] += item

    return lvls


def compare_to_dict(d1, d2):
    ret_value_1 = get_lvls_for_dict(d1)
    ret_value_2 = get_lvls_for_dict(d2)

    for i, j in zip(ret_value_1, ret_value_2):
        if ret_value_1[i] - ret_value_2[j]:
            return False
    return True


def convert_to_utc(time_to_utc):
    return time.mktime(time_to_utc.timetuple())