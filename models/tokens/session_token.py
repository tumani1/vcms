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

        print 'Qr', qr
        if qr is None:
            return None
        else:
            if (datetime.datetime.utcnow() - qr.created < datetime.timedelta(minutes=TOKEN_LIFETIME)) and qr.is_active:
                return qr.id,qr.token,qr.created
            else:
                qr.is_active = False
                session.add(qr)
                session.commit()
                return None

    @classmethod
    def user_is_online(cls, user_id, session=None):
        sess = session.query(cls).filter_by(user_id=user_id).order_by(cls.created.desc()).first()
        return sess and sess.is_active and (datetime.datetime.utcnow() - sess.created < datetime.timedelta(minutes=TOKEN_LIFETIME))



    @classmethod
    def generate_token(cls,user_id,session=None):

        '''
        (Re)Generate token for given user_id
        '''
        qr = session.query(cls).filter(cls.user_id == user_id).first()

        if qr is None:
            gt = cls(user_id=user_id)
            session.add(gt)
            session.commit()
            return gt.id,gt.token,gt.created

        else:
            gt, = qr
            gt.token = cls.token_gen(cls.token_length)
            session.add(gt)
            session.commit()
            return gt.id,gt.token,gt.created
