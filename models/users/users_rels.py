# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

import datetime

from constants import APP_USERSRELS_TYPE, APP_USERSRELS_TYPE_UNDEF
from models import Base


class UsersRels(Base):
    __tablename__ = 'users_rels'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    urStatus   = Column(ChoiceType(choices=APP_USERSRELS_TYPE), nullable=False)
    updated    = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.now)

    def __repr__(self):
        return u"<UsersRels({}-{}:{})>".format(self.user_id, self.partner_id,
                                              self.urStatus)

    @classmethod
    def get_reletion_status(cls, user_id, person_id, session):
        obj = session.query(cls).filter_by(user_id=user_id, partner_id=person_id).first()
        if obj:
            status = obj.urStatus.code
        else:
            status = APP_USERSRELS_TYPE_UNDEF

        return status
