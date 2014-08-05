# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class PersonsMedia(Base):
    __tablename__ = 'persons_media'

    id        = Column(Integer, primary_key=True)
    media_id  = Column(Integer, ForeignKey('media.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    role      = Column(String)
    type    = Column(String)
