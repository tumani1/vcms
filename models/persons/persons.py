# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy_utils import ChoiceType

from models import Base


class Persons(Base):
    __tablename__ = 'persons'

    TYPE_STATUS = (
        (u'1', u'Статус-Дятел'),
        (u'2', u'Статус-Волчара'),
    )

    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    firstname = Column(String(128), nullable=False)
    lastname  = Column(String(128), nullable=False)
    status    = Column(ChoiceType(TYPE_STATUS))
    bio       = Column(Text)

    @property
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)

    def __repr__(self):
        return u"Person(id='{0}', fullname='{1}')>".format(self.id, self.get_full_name)
