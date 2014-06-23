# coding: utf-8
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from models import Base


class Chats(Base):
    __tablename__ = 'chats'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    description = Column(Integer, nullable=False)
    users_chat  = relationship('UsersChat', backref='chat', cascade='all, delete')

    def __repr__(self):
        return u"<Chats([{}] {})>".format(self.id, self.description)