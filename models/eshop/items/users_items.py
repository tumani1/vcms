# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from models import Base


class UsersItems(Base):
    __tablename__ = 'users_items'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    watched = Column(DateTime, nullable=True)
    bought_cnt = Column(Integer, nullable=True)
    wished = Column(DateTime, nullable=True)
    dontlike = Column(DateTime, nullable=True)
