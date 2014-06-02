# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA

from models import Base


class PersonsValues(Base):
    __tablename__ = 'persons_values'

    id           = Column(Integer, primary_key=True)
    scheme_id    = Column(Integer, ForeignKey('scheme.id'), nullable=False)
    person_id    = Column(Integer, ForeignKey('persons.id'), nullable=False)
    value_int    = Column(Integer)
    value_text   = Column(BYTEA)
    value_string = Column(String)


    def __repr__(self):
        return u'<PersonsValues()'.format(self.id, self.person_id.get_full_name)
