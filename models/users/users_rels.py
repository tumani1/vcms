# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

import datetime

from constants import APP_USERSRELS_TYPE, APP_USERSRELS_TYPE_UNDEF
from models import Base
from models.users import Users


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
    def tmpl_for_users_rels(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_reletion_status(cls, user_id, person_id, session):
        obj = session.query(cls).filter_by(user_id=user_id, partner_id=person_id).first()
        if obj:
            status = obj.urStatus.code
        else:
            status = APP_USERSRELS_TYPE_UNDEF

        return status

    @classmethod
    def filter_users_by_status(cls, status, query):
        return query.join(cls, Users.id == cls.user_id).join(cls, cls.partner_id == Users.id).filter(cls.urStatus == status)