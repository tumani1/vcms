# coding: utf-8

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from models.base import Base


class MsgrThreads(Base):
    __tablename__ = 'msgr_threads'
    __table_args__ = {'extend_existing': True}

    id       = Column(Integer, primary_key=True)
    msg_cnt  = Column(Integer, default=0)

    # msgr_thread_users = relationship('UsersMsgrThreads', backref='msgr_threads', cascade='all, delete')
    msgr_thread_logs = relationship('MsgrLog', backref='msgr_threads', cascade='all, delete')

    @classmethod
    def tmpl_for_msgr_threads(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_msgr_threads_by_id(cls, session, msgr_threads_id):
        query = cls.tmpl_for_msgr_threads(session).filter_by(id=msgr_threads_id)

        return query

    def __repr__(self):
        return "<MsgrThreads([{}] {})>".format(self.id, self.msg_cnt)
