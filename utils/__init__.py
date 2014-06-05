

def need_authorization(func):
    def wraper(user, **kwargs):
        if user is None:
            raise NameError('need authorization')
        else:
            return func(user, **kwargs)
    return wraper


