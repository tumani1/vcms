# coding: utf-8
from utils.constants import OBJECT_TYPES
from utils.exceptions import Invalid
from validate_email import validate_email as is_valid_email


def validate_mLimit(limit, **kwargs):
    result = limit.split(',', 1)

    if len(result) == 1:
        if not len(result[0]):
            limit = None
        else:
            limit = int(result[0])
            if limit < 0:
                raise Invalid  # Значение меньше limit
        return limit, 0

    elif len(result) == 2:
        # Check limit
        if not len(result[0]):
            limit = None
        else:
            try:
                limit = int(result[0])
                if limit < 0:
                    raise Invalid  # Значение меньше limit
            except Exception, e:
                limit = None

        # Check top
        try:
            top = int(result[1])
            if top < 0:
                raise Invalid  # Значение меньше top
        except Exception, e:
            top = 0

        return limit, top


def validate_mLimitId(limit):
    mas = limit.split(',', limit.count(','))
    if mas[0] == '':
        mas[0] = 0
    else:
        mas[0] = int(mas[0])
    result = {'limit': mas[0], 'top': 0, 'id_dwn': 0, 'id_top': 0}
    if len(mas) == 4:
        if mas[1] != '':
            result['top'] = int(mas[1])
        else:
            result['top'] = 0

        if mas[2] != '':
            result['id_dwn'] = int(mas[2])
        else:
            result['id_dwn'] = 0

        if mas[3] != '':
            result['id_top'] = int(mas[3])
        else:
            result['id_top'] = 0

    if len(mas) == 3:
        if mas[1] != '':
            result['top'] = int(mas[1])
        else:
            result['top'] = 0

        if mas[2] != '':
            result['id_dwn'] = int(mas[2])
        else:
            result['id_dwn'] = 0

    if len(mas) == 2:
        if mas[1] != '':
            result['top'] = int(mas[1])
        else:
            result['top'] = 0

    if result['limit'] < 0 or result['top'] < 0 or result['id_dwn'] < 0 or result['id_top'] < 0:
        raise Invalid  # Значение меньше 0
    return result


def validate_list_int(value, **kwargs):
    if not isinstance(value, list):
         value = [value]

    try:
        clean_value = [int(i) for i in value]
        if len(clean_value):
            return clean_value

    except Exception, e:
        raise Invalid  # Не целое значение

    return None


def validate_list_string(value, **kwargs):
    if not isinstance(value, list):
       value = [value]

    try:
         clean_value = [str(i).strip() for i in value]
         if len(clean_value):
             return clean_value

    except Exception, e:
        pass

    return None


def validate_string(value, **kwargs):
    try:
        return str(value).strip()
    except Exception, e:
        return None


def validate_int(value, min_value=None, max_value=None, **kwargs):
    try:
        value = int(value)

        if not min_value is None:
            if value < min_value:
                raise Invalid  # Значение меньше min_value

        if not max_value is None:
            if value > max_value:
                raise Invalid  # Значение меньше max_value
    except:
        raise Invalid  # Значение не является целым

    return value


def validate_obj_type(value, **kwargs):
    try:
        obj_type = str(value).strip()
        for item in OBJECT_TYPES:
            if obj_type in item:
                return obj_type
        raise Invalid

    except Exception, e:
        pass


def validate_email(value, **kwargs):
    email = value.strip()
    if is_valid_email(email, check_mx=True):
        return email
    else:
        raise Invalid(u'Некорректный e-mail!')  # Некорректный e-mail


def validate_eshop_price(value, **kwargs):
    try:
        result = [0, 0]
        if isinstance(value, int):
            result = [0, value]
            return result
        elif isinstance(value, str):
            value = value.split(',', 1)
            for i in xrange(2):
                result[i] = int(value[i]) if len(value[i].strip()) else 0
            return result
        else:
            raise Invalid  # Неверный формат цены
    except:
        raise Invalid  # Неверный формат цены


def validate_eshop_sort(value, **kwargs):
    value = value.strip()
    if value == 'name' or value == 'price' or value == 'date':
        return value
    else:
        raise Invalid  # Неверный формат сортировки


def validate_phone_number(value, **kwargs):
    value = value.strip()
    if value.isdigit():
        return value
    else:
        raise Invalid(u'Неверный формат номера!')
