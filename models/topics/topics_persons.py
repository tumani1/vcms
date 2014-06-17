# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models import Base
from models.topics.constants import PERSON_TOPIC_TYPE


class PersonsTopics(Base):
    __tablename__ = 'persons_topics'

    id          = Column(Integer, primary_key=True)
    person_id   = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    topic_name  = Column(String, ForeignKey('topics.name'), nullable=False, index=True)
    role        = Column(String, nullable=False)
    description = Column(Text)
    type        = Column(ChoiceType(PERSON_TOPIC_TYPE))
