from utils import need_authorization

def put(auth_user, **kwargs):
    return kwargs


def get(auth_user, **kwargs):
    return kwargs
@need_authorization
def echo_auth(auth_user, **kwargs):

    return {'message':"Hello,{}".format(user.firstname)}

routes = {'echo':
              {'put': put,
               'get': get},
          'echo_auth':{'get':echo_auth}
    }










