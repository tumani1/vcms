# coding: utf-8
import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime


from models import Base

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    title_orig = Column(String, nullable=True)
    allow_mobile = Column(Boolean, default=False)
    allow_smarttv = Column(Boolean, default=False)
    allow_external = Column(Boolean, default=False)
    allow_anon = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    views_cnt = Column(Integer, nullable=True)
    release_date = Column(DateTime, nullable=True)
    poster = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)


    @classmethod
    def get_media_list(cls, user, session, id=None, text=None, topic=None, releasedate=None, persons=None, units=None):
        query = session.query(cls)

        if not id is None:
            if not isinstance(id, list):
                id = [id]
            query = query.filter(cls.id.in_(id))

        if not text is None:
            query = query.filter(cls.title == text)

        if not releasedate is None:
            query = query.filter(cls.release_date == releasedate)

        return query