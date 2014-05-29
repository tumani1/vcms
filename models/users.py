# coding: utf-8
from sqlalchemy import Column, Text, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy_utils import ChoiceType, PhoneNumberType, TimezoneType, PasswordType

from models import Base


class Users(Base):
    __tablename__ = 'users'

    TYPE_SEX = (
        ('m', u'Мужской'),
        ('w', u'Женский'),
    )

    USER_STATUS = (
        (),
        (),
    )

    id = Column(Integer, primary_key=True)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    sex = Column(ChoiceType(TYPE_SEX))
    phone = Column(PhoneNumberType)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    address = Column(Text)
    time_zone = Column(TimezoneType)
    bio = Column(Text)
    created = Column(DateTime, nullable=False)
    last_visit = Column(DateTime)
    email = Column(String(256))
    password = Column(PasswordType)
    uStatus = Column(ChoiceType(USER_STATUS))
    birthdate = Column(Date)
    uType = Column(String(1))
    userpic_type = Column(String(1))
    userpic_id = Column(Integer)