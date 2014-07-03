# coding: utf-8

def validate_mLimit(limit, **kwargs):
    result = limit.split(',', 1)

    if len(result) == 1:
        limit = int(result[0])
        if limit < 0:
            raise Exception("Значение меньше {0}".format(limit))
        return limit, 0
    elif len(result) == 2:
        # Check limit
        if not len(result[0]):
            limit = None
        else:
            try:
                limit = int(result[0])
                if limit < 0:
                    raise Exception("Значение меньше {0}".format(limit))
            except Exception, e:
                limit = None

        # Check top
        try:
            top = int(result[1])
            if top < 0:
                raise Exception("Значение меньше {0}".format(top))
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

    else:
        if mas[1] != '':
            result['top'] = int(mas[1])
        else:
            result['top'] = 0

    if result['limit'] or result['top'] or result['id_dwn'] or result['id_top'] < 0:
        raise Exception("Значение меньше 0")
    return result

def validate_list_int(value, **kwargs):
    if not isinstance(value, list):
         value = [value]

    try:
        clean_value = [int(i) for i in value]
        if len(clean_value):
            return clean_value

    except Exception, e:
        pass

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
        pass

    return None

def validate_int(value, min_value=None, max_value=None, **kwargs):
   try:
       value = int(value)

       if not min_value is None:
          if value < min_value:
           return Exception("Значение меньше {0}".format(min_value))

       if not max_value is None:
          if value > max_value:
           return Exception("Значение больше {0}".format(max_value))
   except:
       return Exception("Значение не является целым")

   return value
