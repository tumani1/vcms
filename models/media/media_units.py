# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime,\
    and_, SMALLINT, DDL
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship, contains_eager, backref
from sqlalchemy_utils import ChoiceType, TSVectorType

from models.base import Base
from models.media.users_media_units import UsersMediaUnits
from models.media.constants import APP_MEDIA_LIST
from utils.common import user_access_media


class MediaUnits(Base):
    __tablename__ = 'media_units'

    id            = Column(Integer, primary_key=True)
    topic_id      = Column(String, ForeignKey('topics.name'), nullable=False, index=True)
    title         = Column(String, nullable=False)
    title_orig    = Column(String, nullable=True)
    description   = Column(Text, nullable=True)
    previous_unit = Column(Integer, nullable=True)
    next_unit     = Column(Integer, nullable=True)
    release_date  = Column(DateTime, nullable=True)
    end_date      = Column(DateTime, nullable=True)
    batch         = Column(String, nullable=True)
    access        = Column(SMALLINT, default=None, nullable=True)
    access_type   = Column(ChoiceType(APP_MEDIA_LIST), default=None, nullable=True)

    search_name   = Column(TSVectorType('title', 'title_orig', 'description'))

    countries_list   = relationship('MediaUnitsAccessCountries', backref='media_units', cascade='all, delete')
    user_media_units = relationship('UsersMediaUnits', backref='media_units', cascade='all, delete')
    unit_medias      = relationship('MediaInUnit', backref='media_units', cascade='all, delete')
    topic_name       = relationship('Topics', backref=backref('media_units', lazy='dynamic'))


    @classmethod
    def tmpl_for_media_units(cls, user, session):
        query = session.query(cls)

        if not user is None:
            query = query.\
                outerjoin(UsersMediaUnits, and_(cls.id == UsersMediaUnits.media_unit_id, UsersMediaUnits.user_id == user.id)).\
                options(contains_eager(cls.user_media_units))

        return query

    @classmethod
    def get_media_units_list(cls, user, session, id=None, text=None, batch=None, topic=None):
        query = cls.tmpl_for_media_units(user, session)

        if not id is None:
            query = query.filter(cls.id.in_(id))

        if not text is None:
            query = query.filter(cls.title == text)

        if not batch is None:
            query = query.filter(cls.batch == batch)

        if not topic is None:
            query = query.filter(cls.topic_id == topic)

        return query

    @classmethod
    def get_media_unit_by_id(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media_units(user, session).\
            filter(cls.id == id).\
            first()

        return query

    @classmethod
    def get_prev_media_unit(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media_units(user, session).\
            filter(cls.id == session.query(cls.previous_unit).filter(cls.id == id).subquery()).\
            first()

        return query

    @classmethod
    def get_next_media_unit(cls, user, session, id, **kwargs):
        query = cls.tmpl_for_media_units(user, session).\
            filter(cls.id == session.query(cls.next_unit).filter(cls.id == id).subquery()).\
            first()

        return query

    @classmethod
    def access_media_units(cls, media_units, owner, is_auth, is_manager):
        status_code = None
        for media_unit in media_units:
            access = media_unit.access
            status_code = user_access_media(access, owner, is_auth, is_manager)
            if not status_code is None:
                break
        return status_code

    @classmethod
    def get_users_media_unit(cls, user, session, media_id):
        users_media = session.query(UsersMediaUnits).\
            filter_by(user_id=user.id, media_id=media_id).\
            first()

        return users_media

    @classmethod
    def get_search_by_text(cls, session, text, limit=None, **kwargs):
        pass

    def __repr__(self):
        return u'<MediaUnits(id={0}, title={1})>'.format(self.id, self.title)


update_media_units = DDL("""
CREATE FUNCTION media_units_update() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.access_type != OLD.access_type THEN
        DELETE FROM media_units_access_countries WHERE media_unit_id = NEW.id;
    END IF;
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';
CREATE TRIGGER media_units_update BEFORE UPDATE ON media_units
FOR EACH ROW EXECUTE PROCEDURE media_units_update();

CREATE FUNCTION mediaunits_name_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        new.search_name = to_tsvector('pg_catalog.english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.title_orig, '') || ' ' || COALESCE(NEW.description, ''));
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.title <> OLD.title OR NEW.title_orig <> OLD.title_orig OR NEW.description <> OLD.description THEN
            new.search_name =  to_tsvector('pg_catalog.english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.title_orig, '') || ' ' || COALESCE(NEW.description, ''));
        END IF;
    END IF;
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE INDEX mediaunits_search_description_gin_idx ON media_units USING gin(search_name);

CREATE TRIGGER mediaunits_search_name_update BEFORE INSERT OR UPDATE ON media_units
FOR EACH ROW EXECUTE PROCEDURE mediaunits_name_update();
""")

listen(MediaUnits.__table__, 'after_create', update_media_units)
