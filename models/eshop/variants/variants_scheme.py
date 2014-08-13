# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String
from models import Base


class VariantsScheme(Base):
    __tablename__ = 'variants_scheme'

    id = Column(Integer, primary_key=True)
    category_id = Column(ForeignKey('categories.id'), nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    type = Column(Integer, nullable=True)
    default = Column(String, nullable=True)
    enable = Column(Integer, nullable=True)