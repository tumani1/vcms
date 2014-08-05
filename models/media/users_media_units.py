# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from models.base import Base


class UsersMediaUnits(Base):
    __tablename__ = 'users_media_units'

    id            = Column(Integer, primary_key=True)
    media_unit_id = Column(Integer, ForeignKey('media_units.id'), nullable=False)
    user_id       = Column(Integer, ForeignKey('users.id'), nullable=False)
    subscribed    = Column(DateTime, nullable=True)
    watched       = Column(DateTime, nullable=True)

