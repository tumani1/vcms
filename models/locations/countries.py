# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, event
from sqlalchemy.orm import relationship
from pycountry import countries

from models.base import Base


class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = {'extend_existing': True}

    id          = Column(String(2), primary_key=True)
    name        = Column(String(256), unique=True, nullable=False)
    name_orig   = Column(String(256), nullable=False)
    description = Column(Text)

    media_access       = relationship('MediaAccessCountries', backref='location', cascade='all, delete')
    media_type_access  = relationship('MediaAccessDefaultsCountries', backref='location', cascade='all, delete')
    media_units_access = relationship('MediaUnitsAccessCountries', backref='location', cascade='all, delete')

    def __repr__(self):
        return u"<Countries(id={0}, name={1})>".format(self.id, self.name)


def after_create(target, connection, **kw):
    countries_list = []
    for row in countries.objects:
        d = {'id': row.alpha2, 'name': row.name}
        if hasattr(row, 'official_name'):
            d['name_orig'] = row.official_name
        else:
            d['name_orig'] = row.name
        countries_list.append(d)
    insert_sql = target.insert().values(countries_list)
    connection.execute(insert_sql)


event.listen(Countries.__table__, "after_create", after_create)
