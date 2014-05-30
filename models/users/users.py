# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, PhoneNumberType, TimezoneType, PasswordType

from models import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    TYPE_GENDER = (
        ('m', u'Мужской'),
        ('f', u'Женский'),
        ('n', u'Не установлен'),
    )

    TYPE_STATUS = ()

    TYPE_TYPE = ()

    id           = Column(Integer, primary_key=True)
    firstname    = Column(String(128), nullable=False)
    lastname     = Column(String(128), nullable=False)
    gender       = Column(ChoiceType(TYPE_GENDER))
    phone        = Column(PhoneNumberType())
    city_id      = Column(Integer, ForeignKey('cities.id'), nullable=False)
    address      = Column(Text)
    time_zone    = Column(TimezoneType(backend='pytz'))
    bio          = Column(Text)
    created      = Column(DateTime, nullable=False)
    last_visit   = Column(DateTime)
    email        = Column(String(256))
    password     = Column(PasswordType(schemes=['md5_crypt']))
    # uStatus      = Column(ChoiceType(TYPE_STATUS))
    birthdate    = Column(Date)
    # uType        = Column(ChoiceType(TYPE_TYPE))
    userpic_type = Column(String(1))
    userpic_id   = Column(Integer)

    rels         = relationship('UsersRels', backref='users')
    chats        = relationship('UsersChat', backref='users')
    values       = relationship('UsersValues', backref='users')
    msgr_log     = relationship('MsgrLog', backref='users')
    msgr_threads = relationship('UsersMsgrThreads', backref='users')

    def __init__(self):
        pass

    def __repr__(self):
        return '<User([{}] {} {})>'.format(self.id, self.firstname, self.lastname)