# coding: utf-8
import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, and_
from sqlalchemy.orm import relationship, contains_eager
from models import Base
from models.media.users_media import UsersMedia
from models.media.media_in_unit import MediaInUnit
from models.media.persons_media import PersonsMedia
from models.persons.persons import Persons
from models.media.media_units import MediaUnits
from models.media.media_locations import MediaLocations


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

    users_media = relationship('UsersMedia', backref='media', uselist=False)
    media_locations = relationship('MediaLocations', backref='media')

    @classmethod
    def tmpl_for_media(cls, user, session):
        query = session.query(cls)

        if not user is None:
            query = query.\
                outerjoin(UsersMedia, and_(cls.id == UsersMedia.media_id, UsersMedia.user_id == user.id)).\
                options(contains_eager(cls.users_media))
        query = query.\
                outerjoin(MediaLocations, cls.id == MediaLocations.media_id).\
                options(contains_eager(cls.media_locations))
        return query

    @classmethod
    def get_media_list(cls, user, session, id=None, text=None, topic=None, releasedate=None, persons=None, units=None):
        query = cls.tmpl_for_media(user, session)

        if not id is None:
            if not isinstance(id, list):
                id = [id]
            query = query.filter(cls.id.in_(id))

        if not text is None:
            query = query.filter(cls.title == text)

        if not releasedate is None:
            if not isinstance(releasedate, list):
                releasedate = [releasedate]
            if len(releasedate) > 1:
                query = query.filter('extract(\'epoch\' from release_date) >= :start_date AND extract(\'epoch\' from release_date) <= :end_date')\
                    .params(start_date=releasedate[0], end_date=releasedate[1])
            else:
                query = query.filter('extract(\'epoch\' from release_date) = :date').params(date=releasedate[0])

        if not units is None:
            if not isinstance(units, list):
                units = [units]
            subquery = session.query(MediaInUnit.media_id).filter(MediaInUnit.media_unit_id.in_(units)).subquery()
            query = query.filter(cls.id.in_(subquery))

        if not persons is None:
            if not isinstance(persons, list):
                persons = [persons]
            subquery = session.query(PersonsMedia.media_id).filter(PersonsMedia.person_id.in_(persons)).subquery()
            query = query.filter(cls.id.in_(subquery))

        if not topic is None:
            query = query.join(MediaInUnit).join(MediaUnits).filter(MediaUnits.topic_name == topic)
        return query

    @classmethod
    def get_media_by_id(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media(user, session).filter(cls.id == id).first()
        return query

    @classmethod
    def get_persons_by_media_id(cls, user, session, id, limit=None, is_online=None, **kwargs):
        person_ids = []
        persons = session.query(PersonsMedia.person_id).filter(PersonsMedia.media_id.in_(id)).all()
        for person in persons:
            person_ids.append(person[0])
        query = Persons.get_persons_list(session=session, id=person_ids, limit=limit, is_online=is_online)
        query = query.join(PersonsMedia).add_columns(PersonsMedia.role, PersonsMedia.type)
        return query

    @classmethod
    def get_units_by_media_id(cls, user, session, id, **kwargs):
        media_unit_ids = []
        media_units = session.query(MediaUnits.id).join(MediaInUnit).filter(MediaInUnit.media_id == id).all()
        for mu in media_units:
            media_unit_ids.append(mu[0])
        query = MediaUnits.get_media_units_list(user, session, media_unit_ids)
        return query