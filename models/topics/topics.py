# coding: utf-8

from sqlalchemy import Column, String, DateTime
from sqlalchemy_utils import ChoiceType

from models import Base


class Topics(Base):
    __tablename__ = 'topics'

    TOPIC_STATUS = (
        ('a', u'Активен'),
        ('n', u'Не активен'),
    )

    TOPIC_TYPE = (
        ('news', u'Новости'),
        ('show', u'Шоу'),
        ('serial', u'Сериал'),
        ('films', u'Фильмы'),
    )

    name         = Column(String, primary_key=True, nullable=False)
    title        = Column(String, nullable=False)
    title_orig   = Column(String)
    description  = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    status       = Column(ChoiceType(TOPIC_STATUS), nullable=False)
    type         = Column(ChoiceType(TOPIC_TYPE), nullable=False)


    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)
