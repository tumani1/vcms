# coding: utf-8
from sqlalchemy import Column, Integer, String
from models import Base


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Integer, nullable=True)
