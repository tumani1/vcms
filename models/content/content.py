# coding: utf-8

from sqlalchemy import Column, Integer, String, Text
from models import Base


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    obj_type = Column(String, nullable=True)
    obj_id = Column(Integer, nullable=True)
    obj_name = Column(String, nullable=True)


