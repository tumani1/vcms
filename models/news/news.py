# coding: utf-8

import datetime
from sqlalchemy import Column, Integer, DateTime, String
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