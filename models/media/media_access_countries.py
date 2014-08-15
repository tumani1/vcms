# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String

from models.base import Base
from constants import APP_MEDIA_ACCESS_LIST
from utils.constants import HTTP_OK, HTTP_FORBIDDEN


class MediaAccessCountries(Base):
    __tablename__ = 'media_access_countries'

    id         = Column(Integer, primary_key=True)
    media_id   = Column(Integer, ForeignKey('media.id'))
    country_id = Column(String(2), ForeignKey('countries.id'))

    # Проверка доступа видео по стране
    @classmethod
    def access_media(cls, media, country, session):
        if media.access_type is None:
            return None
        access = HTTP_FORBIDDEN
        countries = session.query(cls.country_id).filter_by(media_id=media.id).all()
        if country.id in countries and media.access_type.code == APP_MEDIA_ACCESS_LIST:
            access = HTTP_OK

        return access

    def __repr__(self):
        return u"<MediaAccessLocations(id={0}, media={1}, location={2})>".\
            format(self.id, self.media_id, self.location_id)