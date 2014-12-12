# coding: utf-8
from utils import need_authorization


@need_authorization
def put(auth_user, session=None, **kwargs):
    query = kwargs['query_params']
    password = query.get('password')

    if password:
        auth_user.password = str(password)
        session.add(auth_user)
        session.commit()