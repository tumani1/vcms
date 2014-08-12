# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from models import Base


class UsersItems(Base):
    __tablename__ = 'users_items'
    item_id = Column(ForeignKey('items.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    watched = Column(DateTime, nullable=False)
    bought_cnt = Column(Integer)
    wished = Column(DateTime)
    dontlike = Column(DateTime)
