# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from models import Base


class ExtrasUsers(Base):
    __tablename__ = 'extras_users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    extra_id = Column(Integer, ForeignKey('extras.id'), nullable=False)
    extra_type = Column(Integer, nullable=True)

