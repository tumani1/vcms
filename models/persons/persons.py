# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models import Base
from models.topics.topics_persons import PersonsTopics

from constants import APP_PERSONS_STATUS_TYPE


class Persons(Base):
    __tablename__ = 'persons'

    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey('users.id'), unique=True, index=True)
    firstname = Column(String(128), nullable=False)
    lastname  = Column(String(128), nullable=False)
    status    = Column(ChoiceType(APP_PERSONS_STATUS_TYPE))
    bio       = Column(Text)

    person_topics = relationship('PersonsTopics', backref='persons')


    @classmethod
    def tmpl_for_persons(cls, auth_user, session):
        return session.query(cls)


    @classmethod
    def get_persons_by_id(cls, auth_user, person, session, **kwargs):
        if not isinstance(person, list):
            person = [person]

        query = cls.tmpl_for_persons(auth_user, session).filter(cls.id.in_(person))

        return query


    @classmethod
    def get_persons_list(cls, session, id=None, text=None, is_online=None,
                         is_user=None, limit=None, topic=None, _type=None, **kwargs):

        query = cls.tmpl_for_persons(None, session)

        # Set filter which check that person online
        if not is_online is None:
            pass

        # Set filter by ids
        if not id is None:
            if not isinstance(id, list):
                id = [id]

            query = query.filter(cls.id.in_(id))

        # Set filter which check that person is user
        if not is_user is None:
            query = query.filter(cls.user_id != None)

        # Set filter by text
        if not text is None:
            text_templ = "%{0}%".format(text.upper())
            sql = "(UPPER(persons.firstname::text) LIKE :firstname OR UPPER(persons.lastname::text) LIKE :lastname)"
            query = query.filter(sql).params(firstname=text_templ, lastname=text_templ)

        # Set filter by topic
        if not topic is None:
            query = query.join(PersonsTopics).\
                add_columns(PersonsTopics.topic_name, PersonsTopics.role, PersonsTopics.type).\
                filter(PersonsTopics.topic_name == topic)

            # Set filter by type
            if not _type is None:
                query = query.filter(PersonsTopics.type == _type)

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
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)

    def __repr__(self):
        return u"Person(id='{0}', fullname='{1}')>".format(self.id, self.get_full_name)
