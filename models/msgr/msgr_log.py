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

    def __repr__(self):
        return "<MsgrLog([{}] {} {})>".format(self.id, self.msgr_threads_id, self.user_id)