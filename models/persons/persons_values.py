# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey, and_, or_
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for, listen
from sqlalchemy.dialects.postgresql import BYTEA

from models.base import Base
from models.scheme import Scheme


class PersonsValues(Base):
    __tablename__ = 'persons_values'

    id           = Column(Integer, primary_key=True)
    scheme_id    = Column(Integer, ForeignKey('scheme.id'), nullable=False, index=True)
    person_id    = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    value_int    = Column(Integer)
    value_text   = Column(BYTEA)
    value_string = Column(String)


    @classmethod
    def tmpl_for_values(cls, session):
        return session.query(cls)


    @classmethod
    def get_person_values(cls, person, session, name, value, topic=None):
        if not isinstance(name, list):
            name = [name]

        if not isinstance(value, list):
            value = [value]

        query = cls.tmpl_for_values(session).join(Scheme, and_(cls.scheme_id == Scheme.id, Scheme.name.in_(name))).\
            filter(cls.person_id == person)

        filter_value = cls.validate_value(value)
        if len(filter_value):
            query = query.filter(or_(*filter_value))

        if not topic is None:
            query = query.filter(Scheme.topic_name == topic)

        return query


    @classmethod
    def validate_value(cls, value):
        values_dict = {
            'value_int': [],
            'value_text': [],
            'value_string': [],
        }

        for item in value:
            if isinstance(item, int):
                values_dict['value_int'].append(item)
            elif isinstance(item, basestring):
                if len(item) > 255:
                    values_dict['value_text'].append(item)
                else:
                    values_dict['value_string'].append(item)

        filter_value = []
        for k, v in values_dict.items():
            if not len(v):
                del values_dict[k]
            else:
                filter_value.append(cls.__getattribute__(cls, k).in_(v))

        return filter_value


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
        return u'<PersonsValues(id={0}, person={1}, schema={2})'.format(self.id, self.person_id, self.scheme_id)


def validate_values(mapper, connect, target):
    target.validate_values()

listen(PersonsValues, 'before_insert', validate_values)
