# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

import datetime

from constants import APP_USERSCHAT_TYPE
from models import Base


class UsersChat(Base):
    __tablename__ = 'users_chat '
    __table_args__ = {'extend_existing': True}

    chat_id     = Column(Integer, ForeignKey('chats.id'), primary_key=True)
    chat        = relationship('Chats', backref='users_chat')
    user_id     = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    user        = relationship('Users', backref='users_chat')
    last_update = Column(Integer, onupdate=datetime.datetime.utcnow, default=datetime.datetime.now)
    cuStatus    = Column(ChoiceType(APP_USERSCHAT_TYPE), nullable=False)

    def __repr__(self):
        return "<ChatUser({} {})>".format(self.chat_id, self.user_id)


