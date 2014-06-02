# coding: utf-8

from sqlalchemy import Column, String, DateTime
from sqlalchemy_utils import ChoiceType

from models import Base

class TopicsValues(Base):
    __tablename__ = 'topics_values'


