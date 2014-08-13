# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, Unicode

from models.base import Base
from constants import APP_MEDIA_ACCESS_LIST


class MediaAccessDefaultsCountries(Base):
    __tablename__ = 'media_access_defaults_countries'

    id            = Column(Integer, primary_key=True)
    media_type_id = Column(Unicode, ForeignKey('media_access_defaults.name'))
    country_id    = Column(Integer, ForeignKey('countries.id'))

    # Проверка доступа к видео типу по стране
    @classmethod
    def access_media_type(cls, media_type, country, session):
        if media_type.access_type is None:
            return None
        in_access_list = False
        if country.id in session.query(cls.country_id).filter_by(media_type=media_type).all():
            in_access_list = True
        elif media_type.access_type == APP_MEDIA_ACCESS_LIST:
            return in_access_list
        else:
            return not in_access_list

    def __repr__(self):
        return u"<MediaAccessDefaultsCountries(id={0}, media_type={1}, country={2})>".\
            format(self.id, self.media_type_id, self.country_id)
