# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, String
from models.base import Base


class ExtrasTopics(Base):
    __tablename__ = 'extras_topics'


    id         = Column(Integer, primary_key=True)
    extras_id  = Column(Integer, ForeignKey('extras.id'), nullable=False)
    topic_name = Column(String, ForeignKey('topics.name'), nullable=False)
    extra_type = Column(String)
