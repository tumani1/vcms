# coding: utf-8
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

from constants import APP_USERSOCIAL_TYPE
from models.base import Base


class UsersSocial(Base):
    __tablename__ = 'users_social'

    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sType   = Column(ChoiceType(APP_USERSOCIAL_TYPE), nullable=False)
    sToken  = Column(String(40), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.now)
    social_user_id = Column(Integer, nullable=False)

    def __repr__(self):
        return u'<UsersSocial([{}] {} {})>'.format(self.id, self.user_id, self.sType.code)
