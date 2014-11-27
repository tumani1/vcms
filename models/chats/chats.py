# coding: utf-8

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class Chats(Base):
    __tablename__ = 'chats'
    __table_args__ = {'extend_existing': True}

    id          = Column(Integer, primary_key=True)
    description = Column(String(128), nullable=False)
    users_chats = relationship('UsersChat', backref='chat')

    @classmethod
    def get_new_msgs_count(cls):
        pass

    def __str__(self):
        return u"{} - {}".format(self.id, self.description)

    def __repr__(self):
        return u"<Chats([{}] {})>".format(self.id, self.description)
