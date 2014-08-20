# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, Unicode, String

from models.base import Base
from models.media import MediaAccessDefaults
from utils.constants import HTTP_OK, HTTP_FORBIDDEN


class MediaAccessDefaultsCountries(Base):
    __tablename__ = 'media_access_defaults_countries'

    id            = Column(Integer, primary_key=True)
    media_type_id = Column(Unicode, ForeignKey('media_access_defaults.name'))
    country_id    = Column(String(2), ForeignKey('countries.id'))

    @classmethod
    def access_media_type(cls, media_type_code, country, session):
        media_type = session.query(MediaAccessDefaults).filter_by(name=media_type_code).first()
        if media_type.access_type is None:
            return None
        access = HTTP_FORBIDDEN
        if country.id in session.query(cls.country_id).filter_by(media_type_id=media_type_code).all():
            access = HTTP_OK
        return access

    def __repr__(self):
        return u"<MediaAccessDefaultsCountries(id={0}, media_type={1}, country={2})>".\
            format(self.id, self.media_type_id, self.country_id)
