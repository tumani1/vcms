# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils import ChoiceType

from models import Base


class UsersSocial(Base):
    __tablename__ = 'users_social'

    TYPE_SOCIAL = ()

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sType   = Column(ChoiceType(TYPE_SOCIAL))
    sToken  = Column(String(40))
    created = Column()