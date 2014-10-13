# coding: utf-8
from csv import DictReader
from zipfile import ZipFile

from sqlalchemy import Column, Integer, String, ForeignKey, Text, event
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TimezoneType

import settings
from models.base import Base


class Cities(Base):
    __tablename__ = 'cities'

    id          = Column(Integer, primary_key=True)
    country_id  = Column(String(2), ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    name        = Column(String(256), nullable=False)
    name_orig   = Column(String(256), nullable=True)
    region      = Column(String(10), nullable=False)
    time_zone   = Column(TimezoneType(backend='pytz'), nullable=False, default=u'UTC')
    description = Column(Text)

    country     = relationship('Countries', backref='cities')

    def __repr__(self):
        return u"<Cities(id={0}, name={1})>".format(self.id, self.name)


@event.listens_for(Cities.__table__, 'after_create')
def after_create(target, connection, **kwargs):
    if not settings.TEST:
        with ZipFile(settings.CITIES_ZIP_FILE) as fd_cities, fd_cities.open(settings.CITIES_FILE) as fd:
            csv_dict = DictReader(fd, delimiter=',')
            for row in csv_dict:
                city = {
                    'country_id': row['Country'].upper(),
                    'name_orig': unicode(row['City'].title(), errors='replace'),
                    'region': row['Region'],
                    'name': unicode(row['AccentCity'], errors='replace'),
                }
                insert_query = target.insert().values(city)
                try:
                    connection.execute(insert_query)
                except Exception as e:
                    pass