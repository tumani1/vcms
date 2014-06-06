# coding: utf-8

def validate_mLimit(limit, **kwargs):
    result = limit.split(',', 1)

    if len(result) == 1:
        return result[0], 0
    elif len(result) == 2:
        # Check limit
        if not len(result[0]):
            r1 = None
        else:
            try:
                r1 = int(result[0])
            except Exception, e:
                r1 = None

        # Check top
        try:
            r2 = int(result[1])
        except Exception, e:
            r2 = 0

        return r1, r2
