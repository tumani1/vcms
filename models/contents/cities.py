# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TimezoneType

from models import Base


class Cities(Base):
    __tablename__ = 'cities'
    __table_args__ = {'extend_existing': True}

    id          = Column(Integer, primary_key=True)
    country_id  = Column(Integer, ForeignKey('countries.id'), nullable=False)
    name        = Column(String(256), nullable=False)
    name_orig   = Column(String(256), nullable=False)
    time_zone   = Column(TimezoneType(backend='pytz'), nullable=False)
    description = Column(Text)

    users       = relationship("Users", backref='cities')

    def __init__(self, country, name, name_orig, time_zone, description=None):
        self.country_id = country
        self.name = name
        self.name_orig = name_orig
        self.time_zone = time_zone
        self.description = description

    def __repr__(self):
        return "<Cities([{}] {})>".format(self.id, self.name)
