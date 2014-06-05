# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for, listen
from sqlalchemy.dialects.postgresql import BYTEA

from models import Base


class TopicsValues(Base):
    __tablename__ = 'topics_values'
    __jsonexport__ = ['name', 'value']

    id           = Column(Integer, primary_key=True)
    scheme_id    = Column(Integer, ForeignKey('scheme.id'), nullable=False, index=True)
    topic_name   = Column(String, ForeignKey('topics.name'), nullable=False, index=True)
    value_int    = Column(Integer, nullable=True)
    value_text   = Column(BYTEA, nullable=True)
    value_string = Column(String, nullable=True)


    @classmethod
    def tmpl_for_values(cls, session):
        query = session.query(cls)
        return query

    @classmethod
    def data(cls, data):
        if isinstance(data, list):
            data = [item.to_native() for item in data]
        else:
            data = data.to_native()

        return data


    def to_native(self):
        result = {
            'name': self.topic_name
        }

        value = None
        for item in ['value_int', 'self.value_text', 'self.value_string']:
           if not getattr(self, item) is None:
               value = getattr(self, item)
               break

        result['value'] = value

        return result


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
