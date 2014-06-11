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