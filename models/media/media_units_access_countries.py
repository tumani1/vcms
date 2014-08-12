# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey

from models.base import Base
from constants import APP_MEDIA_ACCESS_LIST


class MediaUnitsAccessCountries(Base):
    __tablename__ = 'media_units_access_countries'

    id            = Column(Integer, primary_key=True)
    media_unit_id = Column(Integer, ForeignKey('media_units.id'))
    country_id    = Column(Integer, ForeignKey('countries.id'))

    @classmethod
    def access_media_unit(cls, media_unit, country, session):
        if media_unit.access_type is None:
            return None
        in_access_list = False
        if country.id in session.query(cls.country_id).filter_by(media_unit_id=media_unit.id).all():
            in_access_list = True
        elif media_unit.access_type == APP_MEDIA_ACCESS_LIST:
            return in_access_list
        else:
            return not in_access_list

    def __repr__(self):
        return u"<MediaUnitsAccessCountries(id={0}, media_unit={1}, country={2})>".\
            format(self.id, self.media_unit_id, self.country_id)
