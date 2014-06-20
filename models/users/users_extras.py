# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint

from models import Base


class UsersExtras(Base):
    __tablename__ = 'users_extras'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'extra_id', name='user_extra_id'), )


    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    extra_id   = Column(Integer, ForeignKey('extras.id'), nullable=False, unique=True)

    def __repr__(self):
        return u"<UsersExtras({}-{})>".format(self.user_id, self.extra_id)