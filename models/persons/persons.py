# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey, select, DDL, Index
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship, column_property
from sqlalchemy_utils import ChoiceType, TSVectorType, Choice
from sqlalchemy_searchable import search

from models.base import Base
from models.topics import PersonsTopics
from models.tokens import SessionToken

from constants import APP_PERSONS_STATUS_TYPE, APP_PERSONS_STATUS_TYPE_ACTIVE


class Persons(Base):
    __tablename__ = 'persons'
    __table_args__ = (
        Index('person_search_name_gin_idx', 'search_name', postgresql_using='gin'),
    )

    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    firstname = Column(String(128), nullable=False)
    lastname  = Column(String(128), nullable=False)
    status    = Column(ChoiceType(APP_PERSONS_STATUS_TYPE), default=APP_PERSONS_STATUS_TYPE_ACTIVE)
    bio       = Column(Text)
    full_name = column_property(firstname + " " + lastname)

    search_name = Column(TSVectorType('firstname', 'lastname', 'bio'))

    person_values = relationship('PersonsValues', backref='persons', cascade='all, delete')
    person_topics = relationship('PersonsTopics', backref='persons', cascade='all, delete')
    person_extras = relationship('PersonsExtras', backref='persons', cascade='all, delete')
    person_medias = relationship('PersonsMedia', backref='persons', cascade='all, delete')


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
            from models.users import Users
            query = SessionToken.filter_users_is_online(is_online=is_online, query=query.join(Users))

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
            query = search(query, text, vector=cls.search_name)

        # Set filter by topic
        if not topic is None:
            query = query.join(PersonsTopics).\
                add_columns(PersonsTopics.role, PersonsTopics.type).\
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
            if limit[1]:
                query = query.offset(limit[1])

        return query

    @classmethod
    def get_search_by_text(cls, session, text, list_ids=None, limit=None, **kwargs):
        if list_ids is None or not len(list_ids):
            return []

        query = cls.tmpl_for_persons(None, session)
        query = query.filter(cls.id.in_(list_ids))

        return query

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

    @property
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)

    def __unicode__(self):
        return u"{0} - {1}".format(self.id, self.get_full_name)

    def __str__(self):
        return "{0} - {1}".format(self.id, self.get_full_name.encode("utf-8"))
    
    def __repr__(self):
        return "Person(id='{0}', fullname='{1}')>".format(self.id, self.get_full_name)


def validate_values(mapper, connect, target):
    # либо поле user_id пустое, либо оно не совпадает с уже имеющимися в таблице user_id
    check = True
    if target.user_id:
        query = select([Persons.user_id]).where(Persons.user_id == target.user_id)
        user_id = connect.execute(query).scalar()
        if user_id == target.user_id:
            check = False

    if not check:
        raise ValueError(u'Необходимо указать уникальный user_id или оставить поле user_id пустым')


listen(Persons, 'before_insert', validate_values)
listen(Persons, 'before_update', validate_values)

update_ts_vector = DDL('''
CREATE FUNCTION person_name_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        new.search_name = to_tsvector(
            'pg_catalog.english',
            CONCAT(
                    REGEXP_REPLACE(COALESCE(NEW.firstname, ''), '[-@.]', ' ', 'g'), ' ',
                    REGEXP_REPLACE(COALESCE(NEW.lastname, ''), '[-@.]', ' ', 'g'), ' ',
                    REGEXP_REPLACE(COALESCE(NEW.bio, ''), '[-@.]', ' ', 'g'), ' '
                )
        );
    END IF;

    IF TG_OP = 'UPDATE' THEN
        IF NEW.bio <> OLD.bio OR NEW.firstname <> OLD.firstname OR NEW.lastname <> OLD.lastname THEN
            new.search_name =  to_tsvector(
                'pg_catalog.english',
                CONCAT(
                    REGEXP_REPLACE(COALESCE(NEW.firstname, ''), '[-@.]', ' ', 'g'), ' ',
                    REGEXP_REPLACE(COALESCE(NEW.lastname, ''), '[-@.]', ' ', 'g'), ' ',
                    REGEXP_REPLACE(COALESCE(NEW.bio, ''), '[-@.]', ' ', 'g'), ' '
                )
            );
        END IF;
    END IF;

    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER persons_search_name_update BEFORE INSERT OR UPDATE ON persons
FOR EACH ROW EXECUTE PROCEDURE person_name_update();
''')

listen(Persons.__table__, 'after_create', update_ts_vector.execute_if(dialect='postgresql'))
