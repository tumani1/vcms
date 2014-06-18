from utils.exceptions import NotAuthorizedException


def need_authorization(func):
    def wraper(*args,**kwargs):
        print args, kwargs
        if (not ('auth_user' in kwargs)) or kwargs['auth_user'] is None:
            func_name = "{} in {}".format(func.func_name,func.func_code.co_filename)
            raise NotAuthorizedException(func_name)
        else:
            return func(*args, **kwargs)
    return wraper


