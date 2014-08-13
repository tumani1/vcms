# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer
from models import Base


class ItemsExtras(Base):
    __tablename__ = 'items_extras'
    item_id = Column(ForeignKey('items.id'), nullable=False)
    extras_id = Column(ForeignKey('extras.id'), nullable=False)
    extras_type = Column(Integer, nullable=True)
