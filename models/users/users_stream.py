# coding: utf-8

import time
import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, UniqueConstraint

from models.base import Base


class UsersStream(Base):
    __tablename__ = 'users_stream'
    __table_args__ = (UniqueConstraint('stream_id', 'user_id', name='stream_user_uc'), )

    id        = Column(Integer, primary_key=True)
    stream_id = Column(Integer, nullable=False)
    user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    liked     = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    @property
    def unixtime(self):
        return time.mktime(self.liked.timetuple())

    def __repr__(self):
        return u'<UsersStream([]-[]:[])>'.format(self.stream_id, self.user_id, self.liked)
