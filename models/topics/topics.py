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

    user_topics = relationship('UsersTopics', backref='topics', uselist=False)


    @classmethod
    def tmpl_for_topics(cls, user, session):
        query = session.query(cls)

        if hasattr(user, 'id'):
            query = query.\
                outerjoin(UsersTopics, and_(cls.name == UsersTopics.topic_name, UsersTopics.user_id == user.id)).\
                options(contains_eager(cls.user_topics))

        return query


    @classmethod
    def get_topics_by_name(cls, user, name, session):
        instance = cls.tmpl_for_topics(user, session).filter(cls.name == name).first()
        return instance


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
                'subscribed': self.user_topics.subscribed,
                'linked': True if self.user_topics.liked else False,
            }

        return result


    @property
    def get_type_code(self):
        return self.type.code


    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)
