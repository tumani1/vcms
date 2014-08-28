# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

import datetime

from constants import APP_USERSCHAT_TYPE, APP_USERSCHAT_TYPE_NULL
from models.base import Base


class UsersChat(Base):
    __tablename__ = 'users_chat'
    __table_args__ = {'extend_existing': True}

    chat_id     = Column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), primary_key=True)
    user_id     = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    last_update = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)
    cuStatus    = Column(ChoiceType(APP_USERSCHAT_TYPE), nullable=False, default=APP_USERSCHAT_TYPE_NULL)


    def __repr__(self):
        return "<UsersChat({} {})>".format(self.chat_id, self.user_id)
