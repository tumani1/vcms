# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

from models import Base

class Extras(Base):
    __tablename__ = 'extras'

    id        = Column(Integer, primary_key=True)
