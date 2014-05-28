# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey

from models import Base


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey(''), nullable=False)
    name = Column(String(256), nullable=False)
    name_orig = Column(String(256), nullable=False)
    time_zone = Column(Integer, nullable=False)

    def __init__(self, country, name, name_orig, time_zone):
        if isinstance(country, int):
            self.country_id = country
        else:
            self.country_id = country.id
        self.name = name
        self.name_orig = name_orig
        self.time_zone = time_zone

