# coding: utf-8
import datetime

from sqlalchemy.sql.expression import func
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, and_, event
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import ChoiceType, PhoneNumberType, TimezoneType, PasswordType, EmailType

from constants import APP_USERS_GENDER_UNDEF, APP_USERS_TYPE_GENDER

from models import Base
from models.contents import Cities, Countries
from models.persons import UsersPersons, Persons
from models.tokens import GlobalToken


class Users(Base):
    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True)
    firstname     = Column(String(128), nullable=False)
    lastname      = Column(String(128), nullable=False)
    gender        = Column(ChoiceType(APP_USERS_TYPE_GENDER), default=APP_USERS_GENDER_UNDEF, nullable=False)
    password      = Column(PasswordType(schemes=['md5_crypt']), nullable=False)
    city_id       = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city          = relationship("Cities", backref='users')
    time_zone     = Column(TimezoneType(backend='pytz'), default=u'UTC')
    created       = Column(DateTime, default=datetime.datetime.utcnow)
    email         = Column(EmailType())
    phone         = Column(PhoneNumberType())
    address       = Column(Text)
    bio           = Column(Text)
    last_visit    = Column(DateTime)
    birthdate     = Column(Date)
    userpic_type  = Column(String(1))
    userpic_id    = Column(Integer)
    # status      = Column(ChoiceType(TYPE_STATUS))
    # type        = Column(ChoiceType(TYPE_TYPE))

    users_values  = relationship('UsersValues', backref='user', cascade='all, delete')
    friends       = relationship('UsersRels', foreign_keys='UsersRels.user_id', backref='user', cascade='all, delete')
    partners      = relationship('UsersRels', foreign_keys='UsersRels.partner_id', backref='partner', cascade='all, delete')
    global_token  = relationship('GlobalToken', backref="users", uselist=False, cascade='all, delete')
    session_token = relationship('SessionToken', backref="users", cascade='all, delete')
    person        = relationship('Persons', backref='users', uselist=False)
    user_persons  = relationship('UsersPersons', backref='users')


    @classmethod
    def tmpl_for_users(cls, session):
        query = session.query(cls)

        return query


    @classmethod
    def get_user_by_person(cls, user_id, person_id, session, **kwargs):
        if not hasattr(user_id, '__iter__'):
            user_id = []

        if not hasattr(person_id, '__iter__'):
            person_id = []

        query = cls.tmpl_for_users(session).filter(cls.id.in_(user_id)).\
            add_columns(UsersPersons.person_id, UsersPersons.subscribed, UsersPersons.liked).\
            outerjoin(UsersPersons, and_(cls.id == UsersPersons.user_id, UsersPersons.person_id.in_(person_id)))

        return query

    @classmethod
    def full_text_search_by_last_first_name(cls, text, session, query=None):
        if query is None:
            query = cls.tmpl_for_users(session)
        return query.filter(func.to_tsvector(func.concat(cls.firstname, " ", cls.lastname)).match(text))

    @classmethod
    def filter_by_cities(cls, city, session, query=None):
        if query is None:
            query = cls.tmpl_for_users(session)
        text = "%{}%".format(city.lower().encode('utf-8'))
        return query.join(Cities).filter(func.lower(Cities.name).like(text))

    @classmethod
    def filter_by_country(cls, country, session, query=None):
        if query is None:
            query = cls.tmpl_for_users(session)
        text = "%{}%".format(country.lower().encode('utf-8'))
        return query.join(Cities).join(Countries).filter(func.lower(Countries.name).like(text))

    @classmethod
    def filter_users_person(cls, is_person, session, query=None):
        if query is None:
            query = cls.tmpl_for_users(session)
        query = query.outerjoin(Persons)
        if is_person:
            query = query.filter(Persons.user_id != None)
        else:
            query = query.filter(Persons.user_id == None)
        return query

    @property
    def get_full_name(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)


    def __repr__(self):
        return u'<User(id={0}, full_name={1})>'.format(self.id, self.get_full_name)


@event.listens_for(Users, 'after_insert')
def create_token_for_user(mapper, connect, target):
    session = sessionmaker(bind=connect)()
    token = GlobalToken.generate_token(target.id, session)