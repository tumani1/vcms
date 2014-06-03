# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

import datetime

from constants import APP_USERSRELS_RELS_TYPE_FRIEND, APP_USERSRELS_RELS_TYPE_SEND_TO, APP_USERSRELS_RELS_TYPE_FROM_USER, APP_USERSRELS_RELS_TYPE_UNDEF
from models import Base


class UsersRels(Base):
    __tablename__ = 'users_rels'
    __table_args__ = {'extend_existing': True}

    RELS_TYPE = (
        (APP_USERSRELS_RELS_TYPE_UNDEF, u'Нет'),
        # это когда сам юзер отправил запрос
        (APP_USERSRELS_RELS_TYPE_SEND_TO, u'Запрос отправлен'),
        # это когда ему другой юзер отправил
        (APP_USERSRELS_RELS_TYPE_FROM_USER, u'запрос отправлен пользователем'),
        (APP_USERSRELS_RELS_TYPE_FRIEND, u'Обоюдная дружба'),
    )

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    urStatus   = Column(ChoiceType(RELS_TYPE), nullable=False)
    update     = Column(DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return "<UsersRels({}-{}:{})>".format(self.user_id, self.partner_id,
                                              self.urStatus)