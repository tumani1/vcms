# coding: utf-8
from utils import need_authorization


@need_authorization
def put(auth_user, password, session=None):
    auth_user.password = str(password)
    session.add(auth_user)
    session.commit()