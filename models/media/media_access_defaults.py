# coding: utf-8
from sqlalchemy import Column, SMALLINT
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models.base import Base
from models.media.constants import APP_MEDIA_TYPE_WITH_DEFAULT, APP_MEDIA_LIST


class MediaAccessDefaults(Base):
    __tablename__ = 'media_access_defaults'

    name        = Column(ChoiceType(APP_MEDIA_TYPE_WITH_DEFAULT), primary_key=True)
    access      = Column(SMALLINT, default=None, nullable=True)
    access_type = Column(ChoiceType(APP_MEDIA_LIST), default=None, nullable=True)

    countries_list = relationship('MediaAccessDefaultsCountries', backref='media_type', cascade='all, delete')

    def __repr__(self):
        return u'<MediaAccessDefaults(name={0})>'.format(self.name)


def after_create(target, connection, **kwargs):
    types = []
    for code, text in APP_MEDIA_TYPE_WITH_DEFAULT:
        d = {'name': code}
        types.append(d)
    insert_sql = target.insert().values(types)
    connection.execute(insert_sql)

listen(MediaAccessDefaults.__table__, 'after_create', after_create)