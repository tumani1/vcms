# coding: utf-8
from sqlalchemy import Column, Integer

from models import Base


class Chats(Base):
    __tablename__ = 'chats'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    description = Column(Integer, nullable=False)

    def __repr__(self):
        return u"<Chats([{}] {})>".format(self.id, self.description)