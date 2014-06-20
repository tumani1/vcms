# coding: utf-8

import time

from sqlalchemy import Column, String, DateTime, and_, DDL# Index
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, TSVectorType

from models import Base
from topics_users import UsersTopics
from models.topics.constants import TOPIC_STATUS, TOPIC_TYPE


class Topics(Base):
    __tablename__ = 'topics'

    name        = Column(String, primary_key=True, nullable=False, index=True)
    title       = Column(String, nullable=False, index=True)
    title_orig  = Column(String)
    description = Column(String, nullable=False)

    releasedate = Column(DateTime, nullable=False)
    status      = Column(ChoiceType(TOPIC_STATUS), nullable=False)
    type        = Column(ChoiceType(TOPIC_TYPE), nullable=False, index=True)

    search_description = Column(TSVectorType('description'), index=True)

    topic_values = relationship('TopicsValues', backref='topics', cascade='all, delete')
    topic_user   = relationship('UsersTopics', backref='topics', cascade='all, delete')
    extra_topics = relationship('ExtrasTopics', backref='topics', cascade='all, delete')
    topic_person = relationship('PersonsTopics', backref='topic', cascade='all, delete')

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
            query = query.filter(cls.search_description == text)

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


    @property
    def get_type_code(self):
        return self.type.code


    @property
    def get_unixtime_created(self):
        return time.mktime(self.releasedate.timetuple())


    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)


update_ts_vector = DDL('''
CREATE FUNCTION topics_desc_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        new.search_description = to_tsvector('pg_catalog.english', COALESCE(NEW.description, ''));
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.description <> OLD.description THEN
            new.search_description = to_tsvector('pg_catalog.english', COALESCE(NEW.description, ''));
        END IF;
    END IF;
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER topics_desc_vector_update BEFORE INSERT OR UPDATE ON topics
FOR EACH ROW EXECUTE PROCEDURE topics_desc_update();
''')

listen(Topics.__table__, 'after_create', update_ts_vector)
