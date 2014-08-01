# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for, listen
from sqlalchemy.dialects.postgresql import BYTEA

from models.base import Base
from models.scheme import Scheme


class TopicsValues(Base):
    __tablename__ = 'topics_values'
    __jsonexport__ = ['name', 'value']

    id           = Column(Integer, primary_key=True)
    scheme_id    = Column(Integer, ForeignKey('scheme.id'), nullable=False, index=True)
    topic_name   = Column(String, ForeignKey('topics.name'), nullable=False, index=True)
    value_int    = Column(Integer)
    value_text   = Column(BYTEA)
    value_string = Column(String)


    @classmethod
    def tmpl_for_values(cls, session):
        return session.query(cls)


    @classmethod
    def get_values_through_schema(cls, session, name, scheme_name):
        if not isinstance(scheme_name, list):
            scheme_name = [scheme_name]

        query = cls.tmpl_for_values(session).join(Scheme).\
            filter(cls.topic_name == name, Scheme.name.in_(scheme_name))

        return query


    # value_int, value_text, value_string - обязательно одни из
    def validate_values(self):
        count = 0
        if self.value_int:
            count += 1
        elif self.value_text:
            count += 1
        elif self.value_string:
            count += 1

        if not count:
            raise ValueError(u'Необходимо указать одно из values полей')

        return self

    def __repr__(self):
        return u'<TopicsValues(schema={0}, topic={1})'.format(self.scheme_id, self.topic_name)


def validate_values(mapper, connect, target):
    target.validate_values()

listen(TopicsValues, 'before_insert', validate_values)
