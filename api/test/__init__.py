def put(user, **kwargs):
    return kwargs


def get(user, **kwargs):
    return kwargs


routes = {'echo':
              {'put': put,
               'get': get}
    }