# coding: utf-8

from sqlalchemy import Column, String, DateTime
from sqlalchemy_utils import ChoiceType

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


    @classmethod
    def get_topics_by_name(cls, user_id, name, session):
        instance = session.query(cls).filter(cls.name==name)
        if not user_id is None:
            instance = instance.outerjoin(UsersTopics)

        return instance


    def __repr__(self):
        return u'Topics(name={0}, type={1}, status={2})'.format(self.name, self.type, self.status)
