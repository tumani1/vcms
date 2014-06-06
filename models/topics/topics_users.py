# coding: utf-8

import time

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from models import Base


class UsersTopics(Base):
    __tablename__ = 'users_topics'
    __table_args__ = (
        UniqueConstraint('user_id', 'topic_name', name='_user_id_topic_name'),
    )

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    topic_name = Column(String, ForeignKey('topics.name'), nullable=False, index=True)
    subscribed = Column(DateTime, nullable=False)
    liked      = Column(DateTime, nullable=True)


    @classmethod
    def tmpl_for_user_topic(cls, session):
        return session.query(cls)


    @classmethod
    def get_user_topic(cls, user, name, session):
        query = cls.tmpl_for_user_topic(session).filter(cls.user_id == user, cls.topic_name == name)
        return query


    @property
    def check_liked(self):
        return time.mktime(self.liked.timetuple()) if not self.liked is None else 0


    @property
    def check_subscribed(self):
        return True if self.subscribed else False


    def __repr__(self):
        return u"<UsersTopics(user={0}, topic={1}, subscr={2})>".format(self.user_id, self.topic_name, self.subscribed)
