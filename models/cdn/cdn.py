# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from models import Base


class CDN(Base):
    __tablename__ = 'cdn'
    name = Column(String, nullable=False, primary_key=True)
    description = Column(String, nullable=True)
    has_mobile = Column(Boolean, nullable=True)
    has_auth = Column(Boolean, nullable=True)
    url = Column(String, nullable=True)
    location_regxp = Column(String, nullable=True)
    cdn_type = Column(String, nullable=True)
