# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey, SMALLINT, Text, Date
from models import Base

class MediaUnits(Base):
    __tablename__ = 'media_units'
    id = Column(Integer, primary_key=True)
    topic_name = Column(String, ForeignKey('topics.name'), nullable=False)
    title = Column(String, nullable=True)
    title_orig = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    previous_unit = Column(Integer, nullable=True)
    next_unit = Column(Integer, nullable=True)
    release_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    batch = Column(String, nullable=True)

    @classmethod
    def tmpl_for_media_units(cls, user, session):
        query = session.query(cls)

        if not user is None:
            query = query.\
                outerjoin(UsersTopics, and_(cls.name == UsersTopics.topic_name, UsersTopics.user_id == user.id)).\
                options(contains_eager(cls.user_topics))

        return query

    @classmethod
    def get_media_units_list(cls, user, session, id=None, text=None, batch=None, topic=None):
        pass

