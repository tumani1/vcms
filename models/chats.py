# coding: utf-8
from sqlalchemy import Column, Integer

from models import Base


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    description = Column(Integer)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "<Chats([{}] {})>".format(self.id, self.description)