# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, PrimaryKeyConstraint
import time
import datetime

from models import Base


class UsersStream(Base):
    __tablename__ = 'users_stream'
    __table_args__ = (PrimaryKeyConstraint('stream_id', 'user_id', name='stream_user_id'), )

    stream_id = Column(String(128), nullable=False)
    user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    liked     = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    @property
    def unixtime(self):
        return time.mktime(self.liked.timetuple())

    def __repr__(self):
        return u'<UsersStream([]-[]:[])>'.format(self.stream_id, self.user_id, self.liked)