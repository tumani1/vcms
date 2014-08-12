# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, Text
from models import Base


class ItemsObjects(Base):
    __tablename__ = 'items_extras'
    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    obj_type = Column(Text, nullable=False)
    obj_id = Column(Integer, nullable=False)
    obj_name = Column(Text, nullable=False)