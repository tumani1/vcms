# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, DateTime, and_
from sqlalchemy.orm import relationship, contains_eager
from sqlalchemy_utils import ChoiceType

from models.base import Base
from models.msgr import MsgrThreads
from constants import TYPE_STATUS


class UsersMsgrThreads(Base):
    __tablename__ = 'users_msgr_threads'
    __table_args__ = {'extend_existing': True}

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey("users.id"))
    msgr_threads_id = Column(Integer, ForeignKey('msgr_threads.id'))
    umtStatus       = Column(ChoiceType(TYPE_STATUS), default=0)
    last_msg_sent   = Column(DateTime)
    last_visit      = Column(DateTime)
    new_msgs        = Column(Integer)

    msgr_threads = relationship('MsgrThreads', backref='users_msgr_threads', cascade='all, delete')

    @classmethod
    def tmpl_for_users_msgr_threads(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def join_with_msgr_threads(cls, user, session, **kwargs):
        user_id = 0
        if not user is None:
            user_id = user.id
        if 'user_authot' in kwargs:
            query = cls.tmpl_for_users_msgr_threads(session).\
                outerjoin(MsgrThreads, and_(UsersMsgrThreads.msgr_threads_id==MsgrThreads.id, UsersMsgrThreads.user_id.in_(kwargs['user_author']))).\
                options(contains_eager(UsersMsgrThreads.msgr_threads)).order_by(UsersMsgrThreads.last_msg_sent)
        else:
            query = cls.tmpl_for_users_msgr_threads(session).\
                outerjoin(MsgrThreads, and_(UsersMsgrThreads.msgr_threads_id==MsgrThreads.id, UsersMsgrThreads.user_id==user_id)).\
                options(contains_eager(UsersMsgrThreads.msgr_threads)).order_by(UsersMsgrThreads.last_msg_sent)

        return query

    @classmethod
    def get_users_msgr_threads_by_user_id(cls, session, users_id):
        query = cls.tmpl_for_users_msgr_threads(session).filter(UsersMsgrThreads.user_id.in_(users_id))
        return query

    @classmethod
    def get_users_msgr_threads_by_msgr_thread_id(cls, session, msgr_thread_id):
        query = cls.tmpl_for_users_msgr_threads(session).filter_by(msgr_threads_id=msgr_thread_id)
        return query

    def __repr__(self):
        return "<UsersMsgrThreads({} {})>".format(self.user_id, self.msgr_threads_id)
