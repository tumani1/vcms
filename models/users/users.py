# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship, contains_eager
from sqlalchemy_utils import ChoiceType, PhoneNumberType, TimezoneType, PasswordType, EmailType, TSVectorType
from sqlalchemy_searchable import make_searchable

import datetime

from constants import APP_USERS_GENDER_UNDEF, APP_USERS_TYPE_GENDER

from models import Base
from models.persons import UsersPersons


make_searchable()


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id           = Column(Integer, primary_key=True)
    firstname    = Column(String(128), nullable=False)
    lastname     = Column(String(128), nullable=False)
    gender       = Column(ChoiceType(APP_USERS_TYPE_GENDER), default=APP_USERS_GENDER_UNDEF, nullable=False)
    password     = Column(PasswordType(schemes=['md5_crypt']), nullable=False)
    city_id      = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city         = relationship("Cities", backref='users')
    time_zone    = Column(TimezoneType(backend='pytz'), default=u'UTC')
    created      = Column(DateTime, default=datetime.datetime.now)
    email        = Column(EmailType())
    phone        = Column(PhoneNumberType())
    address      = Column(Text)
    bio          = Column(Text)
    last_visit   = Column(DateTime)
    birthdate    = Column(Date)
    userpic_type = Column(String(1))
    userpic_id   = Column(Integer)
    # status      = Column(ChoiceType(TYPE_STATUS))
    # type        = Column(ChoiceType(TYPE_TYPE))

    person       = relationship('Persons', backref='users', uselist=False)
    user_persons = relationship('UsersPersons', backref='users', uselist=False)


    @classmethod
    def tmpl_for_users(cls, session):
        query = session.query(cls)

        return query


    @classmethod
    def get_user_by_person(cls, user_id, person_id, session, **kwargs):
        if not hasattr(user_id, '__iter__'):
            user_id = []

        if not hasattr(person_id, '__iter__'):
            person_id = []

        query = cls.tmpl_for_users(session).filter(cls.id.in_(user_id)).\
            outerjoin(UsersPersons, and_(cls.id == UsersPersons.person_id, UsersPersons.person_id.in_(person_id))).\
            options(contains_eager(cls.user_persons))

        return query

    def __repr__(self):
        return u'<User([{}] {} {})>'.format(self.id, self.firstname, self.lastname)

    @property
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)