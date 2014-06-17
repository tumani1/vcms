# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

from models import Base


class PersonsExtras(Base):
    __tablename__ = 'persons_extras'


    id         = Column(Integer, primary_key=True)
    person_id  = Column(Integer, ForeignKey('persons.id'), nullable=False)
    extras_id  = Column(Integer, ForeignKey('extras.id'), nullable=False)
    extra_type = Column(String)

    def __repr__(self):
        return u'<PersonsExtras(person={0}, extras={1}, type={2})>'.format(self.person_id, self.extras_id, self.extra_type)
