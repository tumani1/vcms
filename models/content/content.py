# coding: utf-8

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.event import listen
from sqlalchemy_utils import ChoiceType
from models.base import Base
from models.comments.constants import OBJECT_TYPES


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    obj_type = Column(ChoiceType(OBJECT_TYPES), nullable=False)
    obj_id = Column(Integer, nullable=True)
    obj_name = Column(String, nullable=True)

    @classmethod
    def get_content_list(cls, session, id=None, obj_type=None, obj_id=None, obj_name=None):
        query = session.query(cls)
        if id:
            query = query.filter(cls.id.in_(id))

        if obj_type:
            query = query.filter(cls.obj_type == obj_type)

            if obj_id:
                query = query.filter(cls.obj_id == obj_id)

            if obj_name:
                query = query.filter(cls.obj_name == obj_name)

        return query.all()

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

listen(Content, 'before_insert', validate_object)