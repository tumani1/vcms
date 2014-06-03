# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models import Base


class PersonsTopics(Base):
    __tablename__ = 'persons_topics'

    APP_PERSON_ACTOR = u'actor'
    APP_PERSON_PRODUCER = u'producer'
    APP_PERSON_DIRECTOR = u'director'
    APP_PERSON_SCRIPTWRITER = u'scriptwriter'

    PT_TYPE = (
        (APP_PERSON_ACTOR, u'Актер'),
        (APP_PERSON_PRODUCER, u'Продюсер'),
        (APP_PERSON_DIRECTOR, u'Режиссер'),
        (APP_PERSON_SCRIPTWRITER, u'Сценарист'),
    )

    id           = Column(Integer, primary_key=True)
    person_id   = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    topic_name  = Column(String, ForeignKey('topics.name'), nullable=False, index=True)
    role        = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type        = Column(ChoiceType(PT_TYPE), nullable=True)
