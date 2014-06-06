# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for, listen
from sqlalchemy.dialects.postgresql import BYTEA

from models import Base


class PersonsValues(Base):
    __tablename__ = 'persons_values'

    id           = Column(Integer, primary_key=True)
    scheme_id    = Column(Integer, ForeignKey('scheme.id'), nullable=False, index=True)
    person_id    = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    value_int    = Column(Integer)
    value_text   = Column(BYTEA)
    value_string = Column(String)


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
