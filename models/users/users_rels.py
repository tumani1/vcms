# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

from models import Base


class UsersRels(Base):
    __tablename__ = 'users_rels'

    RELS_TYPE = (
        (0, u'Нет'),
        # это когда сам юзер отправил запрос
        (1, u'Запрос отправлен'),
        # это когда ему другой юзер отправил
        (2, u'запрос отправлен пользователем'),
        (9, u'Обоюдная дружба'),
    )

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    urStatus   = Column(ChoiceType(RELS_TYPE), nullable=False)
    update     = Column(DateTime)

    def __init__(self, user, partner, urStatus, update):
        self.user_id = user
        self.partner_id = partner
        self.urStatus = urStatus
        self.update = update

    def __repr__(self):
        return "<UsersRels({}-{}:{})>".format(self.user_id, self.partner_id,
                                              self.urStatus)