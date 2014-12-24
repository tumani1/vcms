# coding: utf-8

import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, and_, \
    ForeignKey, Boolean, DDL, Float, Index, func
from sqlalchemy.event import listen
from sqlalchemy_utils import ChoiceType, TSVectorType, Choice
from sqlalchemy.orm import relationship, contains_eager, backref
from sqlalchemy_searchable import search

from models.base import Base
from models.media.users_media import UsersMedia
from models.media.media_in_unit import MediaInUnit
from models.media.persons_media import PersonsMedia
from models.persons.persons import Persons
from models.media.media_units import MediaUnits
from models.media.media_locations import MediaLocations
from constants import APP_MEDIA_TYPE, APP_MEDIA_LIST, APP_MEDIA_LIST_ORDER_BY_VIEWS, APP_MEDIA_LIST_ORDER_TYPE_ASC
from utils.common import user_access_media


class Media(Base):
    __tablename__ = 'media'
    __table_args__ = (
        Index('media_search_name_gin_idx', 'search_name', postgresql_using='gin'),
    )

    id             = Column(Integer, primary_key=True)
    title          = Column(String, nullable=False)
    title_orig     = Column(String, nullable=True)
    order          = Column(Integer, nullable=False, default=0)
    allow_mobile   = Column(Boolean, default=True)
    allow_smarttv  = Column(Boolean, default=True)
    allow_external = Column(Boolean, default=True)
    allow_anon     = Column(Boolean, default=True)
    description    = Column(Text, nullable=True)
    created        = Column(DateTime, default=datetime.datetime.utcnow)
    views_cnt      = Column(Integer, default=0)
    rating         = Column(Float, default=0.0)
    rating_votes   = Column(Integer, default=0)
    release_date   = Column(DateTime, nullable=True)
    poster         = Column(Integer, nullable=True)
    duration       = Column(Integer, nullable=True)
    owner_id       = Column(Integer, ForeignKey('users.id'), nullable=False)
    type_          = Column(ChoiceType(APP_MEDIA_TYPE), nullable=False)
    access         = Column(Integer, nullable=True)
    access_type    = Column(ChoiceType(APP_MEDIA_LIST), nullable=True)

    search_name    = Column(TSVectorType('title', 'title_orig', 'description'))

    owner           = relationship('Users', backref=backref('media', lazy='dynamic'))
    countries_list  = relationship('MediaAccessCountries', backref='media', cascade='all, delete')
    users_media     = relationship('UsersMedia', backref='media', cascade='all, delete')
    media_locations = relationship('MediaLocations', backref='media', cascade='all, delete')
    media_units     = relationship('MediaInUnit', backref='media', cascade='all, delete')
    media_persons   = relationship('PersonsMedia', backref='media', cascade='all, delete')

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
    def get_media_list(cls, user, session, id=None, text=None, topic=None,
                       releasedate=None, persons=None, units=None, morder=None,
                       order=None, limit = (12,None,None,None)):

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
            query = query.join(MediaInUnit).join(MediaUnits).filter(MediaUnits.topic_id == topic)

        if not morder is None:
            query = query.join(MediaUnits).filter(MediaInUnit.m_order == morder)

        if not order is None:
            order_column = Media.views_cnt if order['order'] == APP_MEDIA_LIST_ORDER_BY_VIEWS else Media.created
            order_func = order_column.asc if order['order_dir'] == APP_MEDIA_LIST_ORDER_TYPE_ASC else order_column.desc
            query = query.order_by(order_func())

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

    @classmethod
    def get_users_media_by_media(cls, user,  session, id, **kwargs):
        users_media = session.query(UsersMedia).filter(and_(UsersMedia.user_id == user.id, UsersMedia.media_id == id)).first()
        return users_media

    @classmethod
    def access_media(cls, media, owner, is_auth, is_manager):
        access = media.access
        status_code = user_access_media(access, owner, is_auth, is_manager)
        return status_code

    @classmethod
    def mLimitId(cls, elements, limit):
        if limit:
            if limit['id_dwn'] != 0 and limit['id_top'] != 0:
                elements = elements.filter(and_(cls.id <= limit['id_top'], cls.id >= limit['id_dwn']))
            elif limit['id_dwn'] != 0:
                elements = elements.filter(cls.id >= limit['id_dwn'])
            elif limit['id_top']:
                elements = elements.filter(cls.id <= limit['id_top'])
            top, lim = limit['top'], limit['limit']
            if lim:
                elements = elements.limit(lim)
            if top:
                elements = elements.offset(top)

        return elements

    @classmethod
    def get_search_by_text(cls, session, text, list_ids=None, limit=None, **kwargs):
        if list_ids is None or not len(list_ids):
            return []

        query = cls.tmpl_for_media(None, session)
        query = query.filter(cls.id.in_(list_ids))

        return query

    @classmethod
    def media_cnt(cls, session):
        query = session.query(
            func.count(cls.id).label('media_cnt'),
            func.sum(cls.views_cnt).label('views_cnt')
        )

        return query.first()

    @property
    def as_dict(self):
        temp = {}
        for k, v in self.__table__.columns._data.items():
            val = getattr(self, k)
            if isinstance(val, Choice):
                temp[k] = val.code
            else:
                temp[k] = val

        return temp

    def __unicode__(self):
        return u"{0} - {1}".format(self.id, self.title)

    def __str__(self):
        return "{0} - {1}".format(self.id, self.title.encode('utf-8'))

    def __repr__(self):
        return "<Media(id={0}, title={1})>".format(self.id, self.title.encode("utf-8"))

Media.users_media_query = relationship('UsersMedia', lazy='dynamic')

update_access_type = DDL("""
CREATE FUNCTION media_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        new.search_name = to_tsvector('pg_catalog.english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.title_orig, '') || ' ' || COALESCE(NEW.description, ''));
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.title <> OLD.title OR NEW.title_orig <> OLD.title_orig OR NEW.description <> OLD.description THEN
            new.search_name =  to_tsvector('pg_catalog.english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.title_orig, '') || ' ' || COALESCE(NEW.description, ''));
        END IF;
        IF NEW.access_type != OLD.access_type THEN
            DELETE FROM media_access_countries WHERE media_id = NEW.id;
        END IF;
    END IF;
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER media_search_name_update BEFORE INSERT OR UPDATE ON media
FOR EACH ROW EXECUTE PROCEDURE media_update();
""")

listen(Media.__table__, 'after_create', update_access_type)
