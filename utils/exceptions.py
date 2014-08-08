# coding: utf-8
class APIException(Exception):
    """
    Generic API exception
    """
    pass


class RequestErrorException(APIException):
    """
    400
    """
    code = 400
    message = 'Bad Request'


class SessionExpiredException(APIException):
    """
    401
    """
    code = 401
    message = 'Unauthorized'


class NotAuthorizedException(APIException):
    """
    403
    """
    code = 403
    message = 'Forbidden'

    def __str__(self):
        return "Not authorized access"


class NoSuchMethodException(APIException):
    """
    404
    """
    code = 404
    message = 'Not Found'


class WrongHTTPMethod(APIException):
    """
    405
    """
    code = 405
    message = 'Method Not Allowed'


class Http404(APIException):
    """
    404 error
    """
    code = 404
    message = 'Not Found'


class DoesNotExist(APIException):
    """Object does not exist"""
    code = 404
    message = 'Not Found'