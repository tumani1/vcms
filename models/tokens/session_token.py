#coding: utf-8
from sqlalchemy import Column, Boolean

from token import TokenMixin
from settings import TOKEN_LIFETIME

import datetime



class SessionToken(TokenMixin):
    __tablename__ = "session_tokens"

    is_active = Column(Boolean, default=True)

    @classmethod
    def get_user_id_by_token(cls, token_string, session=None):

        qr = session.query(SessionToken.user_id).filter(cls.token == token_string).first()

        if qr is None:
            return None
        else:
            if (datetime.datetime.utcnow() - st.created < datetime.timedelta(minutes=TOKEN_LIFETIME)) and qr.is_active:
                return qr.id,qr.token,
            else:
                qr.is_active = False
                session.add(qr)
                session.commit()
                return None
            

