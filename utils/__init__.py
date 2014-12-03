# coding: utf-8
from utils.exceptions import NotAuthorizedException


def need_authorization(func):

    def wrapper(*args, **kwargs):
        if not kwargs.get('auth_user', None):
            raise NotAuthorizedException
        return func(*args, **kwargs)

    return wrapper