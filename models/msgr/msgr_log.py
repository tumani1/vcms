# coding: utf-8
from sqlalchemy import Column, Integer, String, Binary, ForeignKey

from models import Base


class MsgrLog(Base):
    __tablename__ = 'msgr_log'
    __table_args__ = {'extend_existing': True}

    id              = Column(Integer, primary_key=True)
    msgr_threads_id = Column(Integer, ForeignKey('msgr_threads.id'), nullable=False)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False)
    text            = Column(String(256), nullable=False)
    attachments     = Column(Binary)

    def __init__(self, msgr_threads, user, text, attachments=None):
        self.msgr_threads_id = msgr_threads
        self.user_id = user
        self.text = text
        self.attachments = attachments

    def __repr__(self):
        return "<MsgrLog([{}] {} {})>".format(self.id, self.msgr_threads_id, self.user_id)