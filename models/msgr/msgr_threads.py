# coding: utf-8
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from models import Base


class MsgrThreads(Base):
    __tablename__ = 'msgr_threads'
    __table_args__ = {'extend_existing': True}

    id       = Column(Integer, primary_key=True)
    msg_cnt  = Column(Integer, default=0)

    # msg_logs           = relationship('MsgrLog', backref='msgr_threads')
    # users_msgr_threads = relationship("UsersMsgrThreads", backref='msgr_threads')

    def __repr__(self):
        return "<MsgrThreads([{}] {})>".format(self.id, self.msg_cnt)
