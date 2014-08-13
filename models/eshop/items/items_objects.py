# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, Text
from models import Base


class ItemsObjects(Base):
    __tablename__ = 'items_objects'


    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    obj_type = Column(Text, nullable=True)
    obj_id = Column(Integer, nullable=True)
    obj_name = Column(Text, nullable=True)