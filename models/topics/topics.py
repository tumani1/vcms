# coding: utf-8

import time

from sqlalchemy import Column, String, DateTime, and_, DDL, Index, func
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, TSVectorType, Choice
from sqlalchemy_searchable import search

from models.base import Base
from topics_users import UsersTopics
from models.topics.constants import TOPIC_STATUS, TOPIC_TYPE


class Topics(Base):
    __tablename__ = 'topics'
    __table_args__ = (
        Index('topic_search_name_gin_idx', 'search_name', postgresql_using='gin'),
        Index('topic_search_description_gin_idx', 'search_description', postgresql_using='gin'),
    )

    name        = Column(String, primary_key=True, nullable=False, index=True)
    title       = Column(String, nullable=False, index=True)
    title_orig  = Column(String)
    description = Column(String, nullable=True)
    releasedate = Column(DateTime, nullable=False)
    status      = Column(ChoiceType(TOPIC_STATUS), nullable=False)
    type        = Column(ChoiceType(TOPIC_TYPE), nullable=False, index=True)

    search_description = Column(TSVectorType('description'))
    search_name = Column(TSVectorType('name', 'title', 'title_orig', 'description'))

    topic_values = relationship('TopicsValues', backref='topics', cascade='all, delete')
    topic_user   = relationship('UsersTopics', backref='topics', cascade='all, delete')
    extra_topics = relationship('ExtrasTopics', backref='topics', cascade='all, delete')
    topic_person = relationship('PersonsTopics', backref='topic', cascade='all, delete')
    topic_media  = relationship('MediaUnits', backref='topic', cascade='all, delete')


    @classmethod
    def tmpl_for_topics(cls, auth_user, session):
        query = session.query(cls)

        return query

    @classmethod
    def join_with_user_topics(cls, auth_user, session):
        user_id = 0
        if not auth_user is None:
            user_id = auth_user.id

        query = cls.tmpl_for_topics(auth_user, session).\
            outerjoin(UsersTopics, and_(cls.name == UsersTopics.topic_name, UsersTopics.user_id == user_id)).\
            add_columns(UsersTopics.user_id, UsersTopics.subscribed, UsersTopics.liked)

        return query

    @classmethod
    def get_topics_by_name(cls, auth_user, name, session, **kwargs):
        query = cls.join_with_user_topics(auth_user, session).filter(cls.name == name).first()

        return query

    @classmethod
    def get_topics_list(cls, user, session, name=None, text=None, _type=None, limit=None, **kwargs):
        query = cls.join_with_user_topics(user, session)

        # Set name filter
        if not name is None:
            query = query.filter(cls.name == name)

        # Set description filter
        if not text is None:
            query = query.filter(cls.search_description.op('@@')(func.to_tsquery(text)))

        # Set type filter
        if not _type is None:
            query = query.filter(cls.type == _type)

        # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if limit[1]:
                query = query.offset(limit[1])

        return query

    @classmethod
    def get_search_by_text(cls, session, text, list_ids=None, limit=None, **kwargs):
        if list_ids is None or not len(list_ids):
            return []

        query = cls.tmpl_for_topics(None, session)
        query = query.filter(cls.id.in_(list_ids))

        return query

    @property
    def get_type_code(self):
        return self.type.code

    @property
    def get_unixtime_created(self):
        return time.mktime(self.releasedate.timetuple())

    @property
    def as_dict(self):
        temp = {}
        for k,v in self.__table__.columns._data.items():
            val = getattr(self, k)
            if isinstance(val, Choice):
                temp[k] = val.code
            else:
                temp[k] = val

        return temp

    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)

    def __str__(self):
        return u'{}'.format(self.name)


update_ts_vector = DDL('''
CREATE FUNCTION topics_desc_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        new.search_description = to_tsvector('pg_catalog.english', COALESCE(NEW.description, ''));
        new.search_name = to_tsvector('pg_catalog.english', COALESCE(NEW.description, '') || ' ' || COALESCE(NEW.title_orig, '') || ' ' || COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.name, ''));
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.description <> OLD.description THEN
            NEW.search_description = to_tsvector('pg_catalog.english', COALESCE(NEW.description, ''));
        END IF;

        IF NEW.description <> OLD.description OR NEW.name <> OLD.name OR NEW.title <> OLD.title OR NEW.title_orig <> OLD.title_orig THEN
            NEW.search_name = to_tsvector('pg_catalog.english', COALESCE(NEW.description, '') || ' ' || COALESCE(NEW.title_orig, '') || ' ' || COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.name, ''));
        END IF;
    END IF;
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER topics_desc_vector_update BEFORE INSERT OR UPDATE ON topics
FOR EACH ROW EXECUTE PROCEDURE topics_desc_update();
''')

listen(Topics.__table__, 'after_create', update_ts_vector.execute_if(dialect='postgresql'))
