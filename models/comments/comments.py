# coding: utf-8
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from sqlalchemy.event import listen
from sqlalchemy import event
from sqlalchemy import Column, Integer, String, Text, DateTime, and_
from sqlalchemy_utils import ChoiceType
from models import News

from models.base import Base

from utils.constants import OBJECT_TYPES, OBJECT_TYPE_NEWS


class Comments(Base):
    __tablename__ = 'comments'

    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, nullable=False)
    text        = Column(Text, nullable=False)
    created     = Column(DateTime, nullable=False)
    parent_id   = Column(Integer, nullable=True)
    obj_type    = Column(ChoiceType(OBJECT_TYPES), nullable=False)
    obj_id      = Column(Integer, nullable=True)
    obj_name    = Column(String, nullable=True)

    comment_users = relationship('UsersComments', backref='comments', cascade='all, delete')


    @classmethod
    def get_comments_list(cls, user, session, id=None, user_id=None, obj_type=None, obj_name=None, obj_id=None, **kwargs):
        query = session.query(cls)

        if not id is None:
            query = query.filter(cls.id.in_(id))

        if not user_id is None:
            query = query.filter(cls.user_id.in_(user_id))

        if not obj_type is None:
            query = query.filter(cls.obj_type == obj_type)

            if not obj_id is None:
                query = query.filter(cls.obj_id.in_(obj_id))
            if not obj_name is None:
                query = query.filter(cls.obj_name == obj_name)

        return query

    @classmethod
    def get_comment_by_id(cls, user, session, id):
        query = session.query(cls).filter(cls.id == id).first()
        return query

    @classmethod
    def mLimitId(cls, elements, limit):
        if limit:
            if limit['id_dwn'] != 0 and limit['id_top'] != 0:
                elements = elements.filter(and_(cls.id <= limit['id_top'], cls.id >= limit['id_dwn']))
            elif limit['id_dwn'] != 0:
                elements = elements.filter(cls.id >= limit['id_dwn'])
            elif limit['id_top']:
                elements = elements.filter(cls.id <= limit['id_top'])
            top, lim = limit['top'], limit['limit']
            if lim:
                elements = elements.limit(lim)
            if top:
                elements = elements.offset(top)

        return elements

    def validate_obj(self):
        count = 0
        if self.obj_id:
            count += 1
        elif self.obj_name:
            count += 1

        if not count:
            raise ValueError(u'Необходимо указать obj_id или obj_name')
        return self


@event.listens_for(Comments, 'after_insert')
def increment_news_comments_cnt(mapper, connect, target, **kwargs):
    session = scoped_session(sessionmaker(bind=connect.engine, expire_on_commit=False))()
    if target.obj_type == OBJECT_TYPE_NEWS:
        if target.obj_id:
            news = session.query(News).filter(News.id == target.obj_id).first()
        else:
            news = session.query(News).filter(News.title == target.obj_name).first()
        news.comments_cnt += 1
        session.commit()


@event.listens_for(Comments, 'after_delete')
def decrement_news_comments_cnt(mapper, connect, target):
    session = scoped_session(sessionmaker(bind=connect.engine, expire_on_commit=False))()
    if target.obj_type == OBJECT_TYPE_NEWS:
        if target.obj_id:
            news = session.query(News).filter(News.id == target.obj_id).first()
        else:
            news = session.query(News).filter(News.title == target.obj_name).first()
        if news.comments_cnt > 0:
            news.comments_cnt -= 1
            session.commit()


def validate_object(mapper, connect, target):
    target.validate_obj()

listen(Comments, 'before_insert', validate_object)
