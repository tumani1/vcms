# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

import datetime

from constants import APP_USERSOCIAL_TYPE
from models import Base


class UsersSocial(Base):
    __tablename__ = 'users_social'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user    = relationship('Users', backref='social')
    sType   = Column(ChoiceType(APP_USERSOCIAL_TYPE), nullable=False)
    sToken  = Column(String(40), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, updated=datetime.datetime.now, default=datetime.datetime.now)

    def __repr__(self):
        return u'<UsersSocial([{}] {} {})>'.format(self.id, self.user_id, self.sType.code)