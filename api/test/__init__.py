from utils import need_authorization

def put(user, **kwargs):
    return kwargs


def get(user, **kwargs):
    return kwargs
@need_authorization
def echo_auth(user, **kwargs):

    return "Hello,{}".format(user.firstname)

routes = {'echo':
              {'put': put,
               'get': get},
          'echo_auth':{'get':echo_auth}
    }










