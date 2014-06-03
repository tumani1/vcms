# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, PhoneNumberType, TimezoneType, PasswordType, EmailType

import datetime

from constants import APP_USERS_GENDER_MAN, APP_USERS_GENDER_WOMAN, APP_USERS_GENDER_UNDEF
from models import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    TYPE_GENDER = (
        (APP_USERS_GENDER_MAN, u'Мужской'),
        (APP_USERS_GENDER_WOMAN, u'Женский'),
        (APP_USERS_GENDER_UNDEF, u'Не установлен'),
    )

    id           = Column(Integer, primary_key=True)
    firstname    = Column(String(128), nullable=False)
    lastname     = Column(String(128), nullable=False)
    gender       = Column(ChoiceType(TYPE_GENDER), default=APP_USERS_GENDER_UNDEF)
    password     = Column(PasswordType(schemes=['md5_crypt']), nullable=False)
    city_id      = Column(Integer, ForeignKey('cities.id'), nullable=False)
    created      = Column(DateTime, default=datetime.datetime.now)
    email        = Column(EmailType())
    phone        = Column(PhoneNumberType())
    address      = Column(Text)
    time_zone    = Column(TimezoneType(backend='pytz'))
    bio          = Column(Text)
    last_visit   = Column(DateTime)
    birthdate    = Column(Date)
    userpic_type = Column(String(1))
    userpic_id   = Column(Integer)
    # uStatus      = Column(ChoiceType(TYPE_STATUS))
    # uType        = Column(ChoiceType(TYPE_TYPE))

    # rels         = relationship('UsersRels.user_id', backref='users')
    chats        = relationship('UsersChat', backref='users')
    # values       = relationship('UsersValues', backref='users')
    # msgr_log     = relationship('MsgrLog', backref='users')
    # msgr_threads = relationship('UsersMsgrThreads', backref='users')

    def __repr__(self):
        return '<User([{}] {} {})>'.format(self.id, self.firstname, self.lastname)