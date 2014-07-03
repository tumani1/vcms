# coding: utf-8

def validate_mLimit(limit, **kwargs):
    result = limit.split(',', 1)

    if len(result) == 1:
        return result[0], 0
    elif len(result) == 2:
        # Check limit
        if not len(result[0]):
            limit = None
        else:
            try:
                limit = int(result[0])
            except Exception, e:
                limit = None

        # Check top
        try:
            top = int(result[1])
        except Exception, e:
            top = 0

        return limit, top


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
