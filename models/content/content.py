# coding: utf-8

from sqlalchemy import Column, Integer, String, Text
from models.base import Base


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    obj_type = Column(String, nullable=True)
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
