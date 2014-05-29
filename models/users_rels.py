# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

from models import Base


class UsersRels(Base):
    __tablename__ = 'users_rels'

    RELS_TYPE = (
        ('f', u'Друзья'),
        ('n', u'Никаких')
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    urStatus = Column(ChoiceType(RELS_TYPE), nullable=False)
    update = Column(DateTime)

    def __init__(self, user, partner, urStatus, update):
        self.user_id = user
        self.partner_id = partner
        self.urStatus = urStatus
        self.update = update

    def __repr__(self):
        return "<UsersRels({}-{}:{})>".format(self.user_id, self.partner_id,
                                              self.urStatus)