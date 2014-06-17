# coding: utf-8
import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime


from models import Base

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    title_orig = Column(String, nullable=True)
    allow_mobile = Column(Boolean, default=False)
    allow_smarttv = Column(Boolean, default=False)
    allow_external = Column(Boolean, default=False)
    allow_anon = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    views_cnt = Column(Integer, nullable=True)
    release_date = Column(DateTime, nullable=True)
    poster = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
