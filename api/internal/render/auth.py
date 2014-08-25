# coding: utf-8
from utils import need_authorization
from api.serializers import mUser, mSession


@need_authorization
def get_user_session(auth_user, session, **kwargs):
    return mSession(instance=auth_user.session_token, session=session).data


@need_authorization
def get_auth_user(auth_user, session, **kwargs):
    return mUser(instance=auth_user, session=session).data


@need_authorization
def is_auth(auth_user, **kwargs):
    return not auth_user is None