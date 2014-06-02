# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey

from models import Base


class PersonsTopics(Base):
    __tablename__ = 'persons_topics'

    person_id   = Column(Integer, ForeignKey('persons.id'), nullable=False)
    topic_name  = Column(String, ForeignKey('topics.name'), nullable=False)
    role        = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type        = Column(String, nullable=False)
