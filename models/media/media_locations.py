# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey, SMALLINT
from models import Base


class MediaLocations(Base):
    __tablename__ = 'media_locations'

    id = Column(Integer, primary_key=True)
    cdn_name = Column(String, ForeignKey('cdn.name'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
    quality = Column(String, nullable=True)
    access_level = Column(SMALLINT, nullable=True)
    value = Column(String, nullable=True)
