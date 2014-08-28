# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_utils import ChoiceType

from models.base import Base
from models.extras.constants import APP_PERSONS_EXTRA_TYPE,\
    APP_PERSONS_EXTRA_TYPE_NULL


class PersonsExtras(Base):
    __tablename__ = 'persons_extras'


    id         = Column(Integer, primary_key=True)
    person_id  = Column(Integer, ForeignKey('persons.id'), nullable=False)
    extras_id  = Column(Integer, ForeignKey('extras.id'), nullable=False)
    extra_type = Column(ChoiceType(APP_PERSONS_EXTRA_TYPE), default=APP_PERSONS_EXTRA_TYPE_NULL)


    def __repr__(self):
        return u'<PersonsExtras(person={0}, extras={1}, type={2})>'.format(self.person_id, self.extra_id, self.extra_type)
