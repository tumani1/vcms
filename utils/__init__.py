

def need_authorization(func):
    def wraper(user, *args, **kwargs):
        if user is None:
            raise NameError('need authorization')
        else:
            return func(user, *args, **kwargs)
    return wraper


