# coding: utf-8
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from models import Base


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    description = Column(Integer)

    user_chats = relationship('ChatUsers', backref='chats')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "<Chats([{}] {})>".format(self.id, self.description)