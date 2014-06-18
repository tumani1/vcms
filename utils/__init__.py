from utils.exceptions import NotAuthorizedException


def need_authorization(func):
    def wraper(*args,**kwargs):
        print args, kwargs
        if (not ('auth_user' in kwargs)) or kwargs['auth_user'] is None:
            raise NotAuthorizedException
        else:
            return func(*args, **kwargs)
    return wraper


