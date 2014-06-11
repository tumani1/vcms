from utils.exceptions import NotAuthorizedException


def need_authorization(func):
    def wraper(user, *args, **kwargs):
        if user is None:
            raise NotAuthorizedException
        else:
            return func(user, *args, **kwargs)
    return wraper


