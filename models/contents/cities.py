# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TimezoneType

from models.base import Base


class Cities(Base):
    __tablename__ = 'cities'
    __table_args__ = {'extend_existing': True}

    id          = Column(Integer, primary_key=True)
    country_id  = Column(Integer, ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    name        = Column(String(256), unique=True, nullable=False)
    name_orig   = Column(String(256), nullable=False)
    time_zone   = Column(TimezoneType(backend='pytz'), nullable=False, default=u'UTC')
    description = Column(Text)

    country     = relationship('Countries', backref='cities')


    def __repr__(self):
        return u"<Cities(id={0}, name={1})>".format(self.id, self.name)
