# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from models import Base


class CategoriesExtras(Base):
    __tablename__ = 'categories_extras'

    categories_id = Column(ForeignKey('categories.id'), nullable=False)
    extras_id = Column(ForeignKey('extras.id'), nullable=False)
    extras_type = Column(Integer, nullable=True)
