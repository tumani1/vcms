# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime

from models import Base


class UsersValues(Base):
    __tablename__ = 'users_values'

