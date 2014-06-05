# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from models import Base

class UsersMedia(Base):
    __tablename__ = 'users_media'
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    views_cnt = Column(Integer, nullable=True)
    liked = Column(DateTime, nullable=True)
    playlist = Column(DateTime, nullable=True)
    play_pos = Column(Integer, nullable=True)
    watched = Column(Integer, nullable=True)


