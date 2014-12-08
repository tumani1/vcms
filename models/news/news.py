# coding: utf-8

import datetime
from sqlalchemy import Column, Integer, DateTime, String, desc
from sqlalchemy.event import listen
from models import Base


class News(Base):
    __tablename__ = 'news'
    __table_args__ = {'extend_existing': True}

    id            = Column(Integer, primary_key=True)
    comments_cnt  = Column(Integer, nullable=False)
    published     = Column(DateTime, nullable=True)
    created       = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    text          = Column(String(), nullable=False)
    obj_id        = Column(Integer, nullable=False)
    obj_name      = Column(String(256), nullable=False)
    obj_type      = Column(String(256), nullable=True)

    @classmethod
    def tmpl_for_msgr_threads(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_news_by_id(cls, session, news_id):
        return cls.tmpl_for_msgr_threads(session).filter(cls.id == news_id)

    @classmethod
    def get_news_list(cls, session, id=None, limit=None, sort=None, with_obj=None,
                      obj_type=None, obj_id=None, obj_name=None, **kwargs):

        query = cls.tmpl_for_msgr_threads(session)

        if not id is None:
            query = query.filter(cls.id.in_(id))

        if not obj_type is None:
            query = query.filter(cls.obj_type == obj_type)

        if not obj_name is None:
            query = query.filter(cls.obj_name == obj_name)

        if not obj_id is None:
            query = query.filter(cls.obj_id == obj_id)

        if not sort is None:
            if sort == 'name':
                query = query.order_by(desc(cls.obj_name))
            elif sort == 'date':
                query = query.order_by(desc(cls.created))

        if not limit is None:

            if limit[0]:
                query = query.limit(limit[0])

            if limit[1]:
                query = query.offset(limit[1])

        return query



    def validate_obj(self):
        count = 0
        if self.obj_id:
            count += 1
        elif self.obj_name:
            count += 1

        if not count:
            raise ValueError(u'Необходимо указать obj_id или obj_name')
        return self


def validate_object(mapper, connect, target):
        target.validate_obj()

listen(News, 'before_insert', validate_object)