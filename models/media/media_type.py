# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String

from models.base import Base


class MediaType(Base):
    __tablename__ = 'media_type'

    media_id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    type     = Column(String, ForeignKey('type.type'), primary_key=True)