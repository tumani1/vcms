# coding: utf-8

from sqlalchemy import Column, ForeignKey
from models import Base


class ItemsCategories(Base):
    __tablename__ = 'items_categories'
    item_id = Column(ForeignKey('items.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)

