# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, String
from models.base import Base


class ExtrasMediaUnits(Base):
    __tablename__ = 'extras_mediaunits'


    id           = Column(Integer, primary_key=True)
    extra_id     = Column(Integer, ForeignKey('extras.id'), nullable=False)
    mediaunit_id = Column(String, ForeignKey('media_units.id'), nullable=False)
    extra_type   = Column(String)
