# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, and_
from sqlalchemy.orm import relationship
from sqlalchemy.orm import contains_eager
from sqlalchemy_utils import ChoiceType, PhoneNumberType, TimezoneType, PasswordType, EmailType

import datetime

from constants import APP_USERS_GENDER_UNDEF, APP_USERS_TYPE_GENDER

from models import Base
from models.persons.users_persons import UsersPersons


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
    # uStatus      = Column(ChoiceType(TYPE_STATUS))
    # uType        = Column(ChoiceType(TYPE_TYPE))


    user_persons = relationship('UsersPersons', backref='topics', uselist=False)


    @classmethod
    def tmpl_for_users(cls, session):
        query = session.query(cls)

        return query


    @classmethod
    def get_user_with_person(cls, user, person, session, **kwargs):
        query = cls.tmpl_for_users(session).filter(cls.id == user).\
            outerjoin(UsersPersons, and_(cls.name == UsersPersons.topic_name, UsersPersons.person_id == person)).\
            options(contains_eager(cls.user_persons)).first()

        return query


    @property
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)


    def __repr__(self):
        return u'<User([{}] {} {})>'.format(self.id, self.firstname, self.lastname)
