# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String

from models.base import Base
from models.media.constants import APP_MEDIA_ACCESS_LIST
from utils.constants import HTTP_OK, HTTP_FORBIDDEN


class MediaUnitsAccessCountries(Base):
    __tablename__ = 'media_units_access_countries'

    id            = Column(Integer, primary_key=True)
    media_unit_id = Column(Integer, ForeignKey('media_units.id'))
    country_id    = Column(String(2), ForeignKey('countries.id'))

    @classmethod
    def access_media_unit(cls, media_units, country, session):
        access = None
        for media_unit in media_units:
            if media_unit.access_type is None:
                continue
            countries = [i.country_id for i in session.query(cls.country_id).filter_by(media_unit_id=media_unit.id).all()]
            if country.id in countries:
                if media_unit.access_type.code == APP_MEDIA_ACCESS_LIST:
                    access = HTTP_OK
                else:
                    access = HTTP_FORBIDDEN
                break

        return access

    def __repr__(self):
        return u"<MediaUnitsAccessCountries(id={0}, media_unit={1}, country={2})>".\
            format(self.id, self.media_unit_id, self.country_id)
