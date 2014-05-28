# coding: utf-8
from sqlalchemy import Column, Text, Integer, String, ForeignKey, DateTime

from models import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey(''), nullable=False)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    email = Column(String(256))
    uStatus = Column(String(1))
    created = Column(DateTime(), nullable=False)
    last_visit = Column(DateTime())
    time_zone = Column(Integer())
    phone = Column(String(12))
    country = Column(String(256))
    city = Column(String(256))
    address = Column(String(256))
    birthdate = Column(Integer())
    uType = Column(String(1))
    bio = Column(Text())
    userpic_type = Column(String(1))
    userpic_id = Column(Integer())