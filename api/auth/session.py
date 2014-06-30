# coding: utf-8
from models import SessionToken
from utils import need_authorization
from settings import TOKEN_LIFETIME
import datetime
from utils.serializer import serialize


@need_authorization
@serialize
def get(auth_user, session, **kwargs):
    sid, token, created = SessionToken.generate_token(auth_user.id, session)

    result = {'id': sid,
              'session_token': token,
              'expire': created + datetime.timedelta(minutes=TOKEN_LIFETIME)}
    return result


@need_authorization
def delete(auth_user, session, **kwargs):

    st = session.query(SessionToken).filter(SessionToken.user_id == auth_user.id).first()
    st.is_active = False

    session.add(st)
    session.commit()