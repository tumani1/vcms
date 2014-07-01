# coding: utf-8
from sqlalchemy import Column, Integer, String, Binary, ForeignKey, DateTime

from models import Base


class MsgrLog(Base):
    __tablename__ = 'msgr_log'
    __table_args__ = {'extend_existing': True}

    id              = Column(Integer, primary_key=True)
    msgr_threads_id = Column(Integer, ForeignKey('msgr_threads.id'), nullable=False)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False)
    created         = Column(DateTime, nullable=False)
    text            = Column(String(256), nullable=False)
    attachments     = Column(Binary)


    @classmethod
    def tmpl_for_msgr_log(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_msgr_log_by_id(cls, session, msgr_log_id):
        query = cls.tmpl_for_msgr_threads(session).filter_by(id=msgr_log_id)

        return query

    @classmethod
    def get_msgr_log_by_msgr_thread_id(cls, session, msgr_thread_id):
        query = cls.tmpl_for_msgr_log(session).filter_by(msgr_thread_id=msgr_thread_id)
        return query

    def __repr__(self):
        return "<MsgrLog([{}] {} {})>".format(self.id, self.msgr_threads_id, self.user_id)