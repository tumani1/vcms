# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.event import listens_for, listen
from models import Base


class UsersValues(Base):
    __tablename__ = 'users_values'

    scheme_id    = Column(Integer, ForeignKey('scheme.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    value_int    = Column(Integer)
    value_text   = Column(BYTEA)
    value_string = Column(String)

# value_int, value_text, value_string - обязательно одни из
    def validate_values(self):
        count = 0
        if self.value_int:
            count += 1
        elif self.value_text:
            count += 1
        elif self.value_string:
            count += 1

        if not count:
            raise ValueError(u'Необходимо указать одно из values полей')

        return self


    def __repr__(self):
        return u'<UsersValues(user={1}, schema={2})'.format(self.user_id.get_full_name, self.scheme_id)


def validate_values(mapper, connect, target):
    target.validate_values()

listen(UsersValues, 'before_insert', validate_values)