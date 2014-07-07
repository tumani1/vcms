# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

import datetime

from constants import APP_USERSCHAT_TYPE
from models import Base


class UsersChat(Base):
    __tablename__ = 'users_chat'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    chat_id     = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id     = Column(Integer, ForeignKey('users.id'), nullable=False)
    last_update = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)
    cuStatus    = Column(ChoiceType(APP_USERSCHAT_TYPE), nullable=False)

    def __repr__(self):
        return "<ChatUser({} {})>".format(self.chat_id, self.user_id)
