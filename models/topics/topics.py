# coding: utf-8

from sqlalchemy import Column, String, DateTime, and_
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, TSVectorType

from models import Base
from topics_users import UsersTopics
from models.topics.constants import TOPIC_STATUS, TOPIC_TYPE


class Topics(Base):
    __tablename__ = 'topics'
    __jsonexport__ = ['name', 'title', 'title_orig', 'description', 'releasedate', 'type']

    name        = Column(String, primary_key=True, nullable=False, index=True)
    title       = Column(String, nullable=False, index=True)
    title_orig  = Column(String)
    description = Column(String, nullable=False)

    releasedate = Column(DateTime, nullable=False)
    status      = Column(ChoiceType(TOPIC_STATUS), nullable=False)
    type        = Column(ChoiceType(TOPIC_TYPE), nullable=False, index=True)

    search_description = Column(TSVectorType('description'))

    topic_values = relationship('TopicsValues', backref='topics')
    topic_user   = relationship('UsersTopics', backref='topics')
    # extra_topics = relationship('UsersTopics', backref='topics')


    @classmethod
    def tmpl_for_topics(cls, user, session):
        query = session.query(cls)

        return query


    @classmethod
    def join_with_user_topics(cls, user, session):
        query = cls.tmpl_for_topics(user, session).\
            outerjoin(UsersTopics, and_(cls.name == UsersTopics.topic_name, UsersTopics.user_id == user.id)).\
            add_columns(UsersTopics.user_id, UsersTopics.subscribed, UsersTopics.liked)

        return query


    @classmethod
    def get_topics_by_name(cls, user, name, session, **kwargs):
        query = cls.join_with_user_topics(user, session).filter(cls.name == name).first()

        return query


    @classmethod
    def get_topics_list(cls, user, session, name=None, text=None, _type=None, limit=None, **kwargs):
        query = cls.join_with_user_topics(user, session)

        # Set name filter
        if not name is None:
            query = query.filter(cls.name == name)

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


    @property
    def get_type_code(self):
        return self.type.code


    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)
