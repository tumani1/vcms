# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, SMALLINT
from models.base import Base


class MediaLocations(Base):
    __tablename__ = 'media_locations'

    id           = Column(Integer, primary_key=True)
    cdn_name     = Column(String, ForeignKey('cdn.name'), nullable=False)
    media_id     = Column(Integer, ForeignKey('media.id'), nullable=False)
    quality      = Column(String, nullable=True)
    access_level = Column(SMALLINT, default=None, nullable=True)
    value        = Column(String, nullable=True)

    def __repr__(self):
        return u"<MediaLocation(id={0}, cdn={1}, media={2})>".format(self.id, self.cdn_name, self.media_id)

