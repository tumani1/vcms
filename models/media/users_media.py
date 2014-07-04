# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from models import Base

class UsersMedia(Base):
    __tablename__ = 'users_media'


    id        = Column(Integer, primary_key=True)
    media_id  = Column(Integer, ForeignKey('media.id'), nullable=False)
    user_id   = Column(Integer, ForeignKey('users.id'), nullable=False)
    views_cnt = Column(Integer)
    liked     = Column(DateTime)
    playlist  = Column(DateTime)
    play_pos  = Column(Integer)
    watched   = Column(DateTime)


