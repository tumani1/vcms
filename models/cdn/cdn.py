# coding: utf-8

from sqlalchemy import Column, String, Boolean
from models import Base


class CDN(Base):
    __tablename__ = 'cdn'


    name           = Column(String, primary_key=True)
    description    = Column(String)
    has_mobile     = Column(Boolean)
    has_auth       = Column(Boolean)
    url            = Column(String)
    location_regxp = Column(String)
    cdn_type       = Column(String)


    def __repr__(self):
        return u'<CDN(name={0})>'.format(self.name)
