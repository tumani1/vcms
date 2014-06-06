# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

from constants import APP_USERSEXTRAS_TYPE
from models import Base


class UsersExtras(Base):
    __tablename__ = 'users_extras'
    __table_args__ = {'extend_existing': True}

    user_id    = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user       = relationship('Users', foreign_keys=user_id, backref='users_extras')
    extra_id   = Column(Integer, ForeignKey('extras.id'), nullable=False, unique=True)
    extra      = relationship('Extras', backref='users_extras')
    extra_type = Column(ChoiceType(APP_USERSEXTRAS_TYPE), nullable=False)

    def __repr__(self):
        return u"<UsersExtras({}-{}:{})>".format(self.user_id, self.extra_id,
                                              self.extra_type.code)