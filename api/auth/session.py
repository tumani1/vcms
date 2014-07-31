# coding: utf-8

import datetime

from models.tokens import SessionToken

from settings import TOKEN_LIFETIME

from utils import need_authorization
from utils.serializer import serialize


@need_authorization
@serialize
def get(auth_user, session, **kwargs):
    sid, token, created = SessionToken.generate_token(auth_user.id, session)
    auth_user.last_visit = datetime.datetime.utcnow()
    session.add(auth_user)
    session.commit()
    result = {'id': sid,
              'session_token': token,
              'expire': created + datetime.timedelta(minutes=TOKEN_LIFETIME)}
    return result


@need_authorization
def delete(auth_user, session, **kwargs):
    auth_user.last_visit = datetime.datetime.utcnow()
    st = session.query(SessionToken).filter(SessionToken.user_id == auth_user.id).first()
    st.is_active = False
    session.add_all((st, auth_user))
    session.commit()
