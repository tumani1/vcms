# coding: utf-8
import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime


from models import Base

class Extras(Base):
    __tablename__ = 'extras'
    id = Column(Integer, primary_key=True)
    cdn_name = Column(String, ForeignKey('cdn.name'), nullable=False)
    e_type = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.datetime.now)
    description = Column(Text, nullable=True)
    title = Column(String, nullable=True)
    title_orig = Column(String, nullable=True)
