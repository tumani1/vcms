from utils import need_authorization


def put(auth_user, session, **kwargs):
    return kwargs


def get(auth_user, session, **kwargs):
    return kwargs


@need_authorization
def echo_auth(auth_user, **kwargs):

    return {'message': "Hello,{}".format(auth_user.firstname)}

routing = (
    (r'^echo$', {'put': put, 'get': get}),
    (r'^echoauth$', {'get': echo_auth}),
)










