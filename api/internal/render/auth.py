# coding: utf-8
from utils import need_authorization
from utils.exceptions import RequestErrorException

from api.serializers import mUser, mSession
from models.tokens import SessionToken


@need_authorization
def get_user_session(auth_user, session, query_params, **kwargs):
    if 'token' in query_params:
        session_token = session.query(SessionToken).filter_by(token=query_params['token']).first()
        return mSession(instance=session_token, session=session).data
    else:
        raise RequestErrorException


@need_authorization
def get_auth_user(auth_user, session, **kwargs):
    return mUser(instance=auth_user, session=session).data


def is_auth(auth_user, **kwargs):
    return not auth_user is None