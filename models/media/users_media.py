# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from models.base import Base


class UsersMedia(Base):
    __tablename__ = 'users_media'

    id        = Column(Integer, primary_key=True)
    media_id  = Column(Integer, ForeignKey('media.id'), nullable=False)
    user_id   = Column(Integer, ForeignKey('users.id'), nullable=False)
    views_cnt = Column(Integer, default=0)
    liked     = Column(DateTime)
    playlist  = Column(DateTime)
    play_pos  = Column(Integer)
    watched   = Column(DateTime)

    def __repr__(self):
        return u'<UsersMedia(id={0}, media={1}, user={2})>'.format(self.id, self.media_id, self.user_id)
