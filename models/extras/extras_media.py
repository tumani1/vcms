# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, String
from models.base import Base


class ExtrasMedia(Base):
    __tablename__ = 'extras_media'


    id         = Column(Integer, primary_key=True)
    extras_id  = Column(Integer, ForeignKey('extras.id'), nullable=False)
    media_id   = Column(Integer, ForeignKey('media.id'), nullable=False)
    extra_type = Column(String)
