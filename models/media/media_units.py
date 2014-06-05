# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey, SMALLINT, Text, Date
from models import Base

class MediaUnits(Base):
    __tablename__ = 'media_units'
    id = Column(Integer, primary_key=True)
    topic_name = Column(String, ForeignKey('topics.name'), nullable=False)
    title = Column(String, nullable=True)
    title_orig = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    previous_init = Column(Integer, nullable=True)
    next_unit = Column(Integer, nullable=True)
    release_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    batch = Column(String, nullable=True)

