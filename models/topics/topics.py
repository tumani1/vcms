# coding: utf-8

from sqlalchemy import Column, String, DateTime, and_
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

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

    topic_values = relationship('TopicsValues', backref='topics')
    topic_user = relationship('UsersTopics', backref='topics', uselist=False)
    # extra_topics = relationship('UsersTopics', backref='topics')


    @classmethod
    def tmpl_for_topics(cls, user, session):
        query = session.query(cls)

        if hasattr(user, 'id'):
            query = query.\
                outerjoin(UsersTopics, and_(cls.name == UsersTopics.topic_name, UsersTopics.user_id == user.id)).\
                options(contains_eager(cls.user_topics))

        return query


    @classmethod
    def get_topics_by_name(cls, user, name, session, **kwargs):
        query = cls.tmpl_for_topics(user, session).filter(cls.name == name).first()
        return query


    @classmethod
    def get_topics_list(cls, user, session, name=None, text=None, _type=None, limit=None, **kwargs):
        query = cls.tmpl_for_topics(user, session)

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


    @classmethod
    def get_topics_extras(cls, user, session, name=None, text=None, _type=None, limit=None, **kwargs):
        query = session.query(cls)

        return query


    @classmethod
    def data(cls, user, data):
        if isinstance(data, list):
            data = [item.to_native(user) for item in data]
        else:
            data = data.to_native(user)

        return data


    def to_native(self, user):
        result = dict(zip(self.__jsonexport__, [getattr(self, v) for v in self.__jsonexport__]))
        result['type'] = result['type'].code

        result['relation'] = {}
        if hasattr(user, 'id') and not self.user_topics is None:
            result['relation'] = {
                'subscribed': self.topic_user.subscribed,
                'liked': self.topic_user.check_liked,
            }

        return result


    @property
    def get_type_code(self):
        return self.type.code


    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)