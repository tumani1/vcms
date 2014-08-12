# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey

from models.base import Base
from constants import APP_MEDIA_ACCESS_LIST


class MediaAccessCountries(Base):
    __tablename__ = 'media_access_countries'

    id         = Column(Integer, primary_key=True)
    media_id   = Column(Integer, ForeignKey('media.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))

    # Проверка доступа видео по стране
    @classmethod
    def access_media(cls, media, country, session):
        if media.access_type is None:
            return None
        in_access_list = False
        if country.id in session.query(cls.country_id).filter_by(media_id=media.id).all():
            in_access_list = True
        elif media.access_type == APP_MEDIA_ACCESS_LIST:
            return in_access_list
        else:
            return not in_access_list

    def __repr__(self):
        return u"<MediaAccessLocations(id={0}, media={1}, location={2})>".\
            format(self.id, self.media_id, self.location_id)