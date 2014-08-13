# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer
from models import Base


class ItemsCategories(Base):
    __tablename__ = 'items_categories'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)

