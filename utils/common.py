# coding: utf-8

import re
import time

from models.media.constants import APP_ACCESS_LEVEL_MANAGER_MASK,\
    APP_ACCESS_LEVEL_OWNER_MASK, APP_ACCESS_LEVEL_GUEST_MASK,\
    APP_ACCESS_LEVEL_AUTH_USER_MASK

from utils.constants import HTTP_OK, HTTP_FORBIDDEN
from utils.exceptions import NoSuchMethodException


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


def detetime_to_unixtime(time_to_utc):
    return time.mktime(time_to_utc.utctimetuple())


def get_or_create(session, model, create=None, filter=None):
    instance = session.query(model).filter_by(**(filter or {})).first()
    if instance:
        return instance, False
    else:
        instance = model(**create)
        session.add(instance)
        return instance, True


def user_access_media(access, owner, is_auth, is_manager):
    status_code = None
    if access:
        if is_auth:
            if owner and (access & APP_ACCESS_LEVEL_OWNER_MASK) != 0:
                status_code = HTTP_OK
            elif is_manager and (access & APP_ACCESS_LEVEL_MANAGER_MASK) != 0:
                status_code = HTTP_OK
            elif (access & APP_ACCESS_LEVEL_AUTH_USER_MASK) != 0:
                status_code = HTTP_OK
            else:
                status_code = HTTP_FORBIDDEN
        elif (access & APP_ACCESS_LEVEL_GUEST_MASK) != 0:
            status_code = HTTP_OK
        else:
            status_code = HTTP_FORBIDDEN
    return status_code


def get_api_by_url(routes, IPC_pack):
        path_parse = IPC_pack['api_method'].split('/', 2)

        group = routes.get(path_parse[1])
        if group is None:
            raise NoSuchMethodException

        for item in group:
            method = IPC_pack['api_type'].lower()
            match = re.match(item[0], u'/'.join(path_parse[2:]))

            if match and method in item[1]:
                return match.groupdict(), item[1][method]

        raise NoSuchMethodException
