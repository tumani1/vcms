# coding: utf-8

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
