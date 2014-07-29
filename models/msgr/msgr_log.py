# coding: utf-8
from sqlalchemy import Column, Integer, String, Binary, ForeignKey, DateTime, and_
import datetime

from models import Base


class MsgrLog(Base):
    __tablename__ = 'msgr_log'
    __table_args__ = {'extend_existing': True}

    id              = Column(Integer, primary_key=True)
    msgr_threads_id = Column(Integer, ForeignKey('msgr_threads.id'), nullable=False)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False)
    created         = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
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
        query = cls.tmpl_for_msgr_log(session).filter_by(msgr_threads_id=msgr_thread_id)
        return query

    @classmethod
    def get_msgr_log_by_msgr_thread_id_and_user_id(cls, session, msgr_thread_id, user_id):
        query = cls.tmpl_for_msgr_log(session).filter(and_(cls.msgr_threads_id==msgr_thread_id, cls.user_id==user_id))
        return query

    @classmethod
    def get_msgr_log_by_msgr_thread_id_limit(cls, session, msgr_thread_id, limit):
        if limit['id_dwn'] != 0 and limit['id_top'] != 0:
            query = cls.tmpl_for_msgr_log(session).filter(and_(limit['id_top'] >= cls.id, cls.id>=limit['id_dwn']), cls.msgr_threads_id==msgr_thread_id)
        elif limit['id_dwn'] != 0:
            query = cls.tmpl_for_msgr_log(session).filter(cls.id>=limit['id_dwn'], cls.msgr_threads_id==msgr_thread_id)
        else:
            query = cls.tmpl_for_msgr_log(session).filter(limit['id_top']>=cls.id, cls.msgr_threads_id==msgr_thread_id)

        query = cls.query_filling(query, limit['limit'], limit['top'])

        return query

    @classmethod
    def query_filling(cls, query, limit, top):
        # Set Limit
        if limit:
            query = query.limit(limit)

        # Set Offset
        if top:
            query = query.offset(top)

        return query

    def __repr__(self):
        return "<MsgrLog([{}] {} {})>".format(self.id, self.msgr_threads_id, self.user_id)