# coding: utf-8

import time
import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, and_
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from models.extras.constants import APP_EXTRA_TYPE

from models import Base
from models.extras.extras_topics import ExtrasTopics
from models.extras.extras_persons import PersonsExtras


class Extras(Base):
    __tablename__ = 'extras'


    id          = Column(Integer, primary_key=True)
    cdn_name    = Column(String, ForeignKey('cdn.name'), nullable=False)
    cdn         = relationship('CDN', backref='extras')
    type        = Column(ChoiceType(APP_EXTRA_TYPE), nullable=False)
    location    = Column(String, nullable=False)
    created     = Column(DateTime, default=datetime.datetime.now)
    description = Column(Text, nullable=False)
    title       = Column(String, nullable=False)
    title_orig  = Column(String, nullable=False)


    @classmethod
    def tmpl_for_extras(cls, session):
        return session.query(cls)


    @classmethod
    def query_filling(cls, query, id=None, text=None, _type=None, limit=None):
        # Set name filter
        if not id is None:
            query = query.filter(cls.id.in_(id))

        # Set description filter
        if not text is None:
        #     query = query.filter(cls.description == text)
            pass

        # Set type filter
        if not _type is None:
            query = query.filter(cls.type == _type)

        # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if not limit[0] is None:
                query = query.offset(limit[1])

        return query


    @classmethod
    def get_extras_by_topics(cls, name, session, id=None, text=None, _type=None, limit=None):
        query = cls.tmpl_for_extras(session).\
            join(ExtrasTopics, and_(cls.id == ExtrasTopics.extras_id, ExtrasTopics.topic_name == name))

        # Конструктор запроса
        query = cls.query_filling(query, id=None, text=None, _type=None, limit=None)

        return query


    @classmethod
    def get_extras_by_person(cls, person, session, id=None, text=None, _type=None, limit=None):
        query = cls.tmpl_for_extras(session).\
            join(PersonsExtras, and_(cls.id == ExtrasTopics.extras_id, PersonsExtras.person_id == person))

        # Конструктор запроса
        query = cls.query_filling(query, id=None, text=None, _type=None, limit=None)

        return query


    @classmethod
    def data(cls, data):
        if isinstance(data, list):
            data = [item.to_native() for item in data]
        else:
            data = data.to_native()

        return data


    def to_native(self):
        result = {
            'id': self.id,
            'type': self.get_type_code,
            'title': self.title,
            'title_orig': self.title_orig,
            'description': self.description,
            'location': self.location,
            'created': self.get_by_created_unixtime,
        }

        return result


    @property
    def get_type_code(self):
        return self.type.code


    @property
    def get_by_created_unixtime(self):
        return time.mktime(self.created.timetuple())
