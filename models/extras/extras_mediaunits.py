# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, String
from models.base import Base


class ExtrasMediaUnits(Base):
    __tablename__ = 'extras_media_units'


    id            = Column(Integer, primary_key=True)
    extras_id     = Column(Integer, ForeignKey('extras.id'), nullable=False)
    media_unit_id = Column(Integer, ForeignKey('media_units.id'), nullable=False)
    extra_type    = Column(String)
