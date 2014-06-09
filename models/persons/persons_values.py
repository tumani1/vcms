# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for, listen
from sqlalchemy.dialects.postgresql import BYTEA

from models import Base
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
    def get_values_through_schema(cls, session, name, scheme_name):
        if not isinstance(scheme_name, list):
            scheme_name = [scheme_name]

        query = cls.tmpl_for_values(session).join(Scheme).\
            filter(cls.topic_name == name, Scheme.name.in_(scheme_name))

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
        return u'<PersonsValues(id={0}, person={1}, schema={2})'.format(self.id, self.person_id, self.scheme_id)


def validate_values(mapper, connect, target):
    target.validate_values()

listen(PersonsValues, 'before_insert', validate_values)
