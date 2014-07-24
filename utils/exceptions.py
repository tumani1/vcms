# coding: utf-8
class RequestErrorException(Exception):
    """
    400
    """
    pass


class SessionExpiredException(Exception):
    """
    401
    """
    pass


class NotAuthorizedException(Exception):
    """
    403
    """
    def __str__(self):
        return "Not authorized access"


class NoSuchMethodException(Exception):
    """
    404
    """
    pass


class WrongHTTPMethod(Exception):
    """
    405
    """
    pass


class Http404(Exception):
    """
    404 error
    """


class DoesNotExist(Exception):
    """Object does not exist"""
    pass
