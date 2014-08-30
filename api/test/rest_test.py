# coding: utf-8
from utils import need_authorization


def put(**kwargs):
    return kwargs['query_params']


def get(**kwargs):
    return kwargs['query_params']


@need_authorization
def echo_auth(auth_user, **kwargs):

    return {'message': "Hello,{}".format(auth_user.firstname)}
