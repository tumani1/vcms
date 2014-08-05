# coding: utf-8
from utils import need_authorization


@need_authorization
def put(auth_user, session=None, **kwargs):
    query = kwargs['query']
    if 'password' in query:
        password = str(query['password'])
        auth_user.password = str(password)
        session.add(auth_user)
        session.commit()