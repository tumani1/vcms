# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models import Base
from constants import APP_PERSONS_STATUS_TYPE


class Persons(Base):
    __tablename__ = 'persons'

    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey('users.id'), index=True)
    firstname = Column(String(128), nullable=False)
    lastname  = Column(String(128), nullable=False)
    status    = Column(ChoiceType(APP_PERSONS_STATUS_TYPE))
    bio       = Column(Text)

    user      = relationship('Users', foreign_keys=user_id, backref='person')


    @classmethod
    def tmpl_for_persons(cls, user, session):
        return session.query(cls)


    @classmethod
    def get_persons_by_id(cls, user, person, session, **kwargs):
        if not isinstance(person, list):
            person = [person]

        query = cls.tmpl_for_persons(user, session).filter(cls.id.in_(person))

        return query


    @property
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)

    def __repr__(self):
        return u"Person(id='{0}', fullname='{1}')>".format(self.id, self.get_full_name)
