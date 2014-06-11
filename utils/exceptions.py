# coding: utf-8
class RequestErrorException(Exception):
    pass

class SessionExpiredException(Exception):
    pass

class NotAuthorizedException(Exception):
    pass

class NoSuchMethodException(Exception):
    pass

class WrongHTTPMethod(Exception):
    pass

class Http404(Exception):
    """
    404 error
    """

class DoesNotExist(Exception):
    """Object does not exist"""
    pass
