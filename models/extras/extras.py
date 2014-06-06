# coding: utf-8

import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from models.extras.constants import EXTRA_TYPE

from models import Base


class Extras(Base):
    __tablename__ = 'extras'


    id          = Column(Integer, primary_key=True)
    cdn_name    = Column(String, ForeignKey('cdn.name'), nullable=False)
    type        = Column(ChoiceType(EXTRA_TYPE), nullable=False)
    location    = Column(String, nullable=True)
    created     = Column(DateTime, default=datetime.datetime.now)
    description = Column(Text, nullable=True)
    title       = Column(String, nullable=False)
    title_orig  = Column(String, nullable=True)
