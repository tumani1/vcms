# coding: utf-8
from sqlalchemy import Column, Integer, String

from models import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    name_orig = Column(String(256), nullable=False)

    def __init__(self, name, name_orig):
        self.name = name
        self.name_orig = name_orig

