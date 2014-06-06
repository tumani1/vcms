# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

import datetime

from constants import APP_USERSRELS_TYPE
from models import Base


class UsersRels(Base):
    __tablename__ = 'users_rels'
    __table_args__ = {'extend_existing': True}

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    user       = relationship('Users', foreign_keys=user_id, backref='friends')
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    partner    = relationship('Users', foreign_keys=partner_id, backref='partners')
    urStatus   = Column(ChoiceType(choices=APP_USERSRELS_TYPE), nullable=False)
    updated    = Column(DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)

    def __repr__(self):
        return u"<UsersRels({}-{}:{})>".format(self.user_id, self.partner_id,
                                              self.urStatus)