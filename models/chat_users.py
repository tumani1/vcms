# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String

from models import Base


class ChatUsers(Base):
    __tablename__ = 'chat_users'

    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    last_update = Column(Integer)
    cuStatus = Column(String(128))

    def __init__(self, chat, user, last_update=None, cuStatus=None):
        self.chat_id = chat
        self.user_id = user
        self.last_update = last_update
        self.cuStatus = cuStatus

    def __repr__(self):
        return "<ChatUser({} {})>".format(self.chat_id, self.user_id)


