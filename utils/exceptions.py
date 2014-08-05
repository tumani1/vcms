# coding: utf-8


class APIException(Exception):
    """
    Generic API exception
    """

    code = 404


class RequestErrorException(APIException):
    """
    400
    """
    code = 400


class SessionExpiredException(APIException):
    """
    401
    """
    code = 401


class NotAuthorizedException(APIException):
    """
    403
    """
    code = 403

    def __str__(self):
        return "Not authorized access"


class NoSuchMethodException(APIException):
    """
    404
    """
    code = 404


class WrongHTTPMethod(APIException):
    """
    405
    """
    code = 405


class Http404(APIException):
    """
    404 error
    """
    code = 404