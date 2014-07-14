# coding: utf-8
from models import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy_utils import ChoiceType
from constants import OBJECT_TYPES

class Comments(Base):
    __tablename__ = 'comments'
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, nullable=False)
    text        = Column(Text, nullable=False)
    created     = Column(DateTime, nullable=False)
    parent_id   = Column(Integer, nullable=True)
    obj_type    = Column(ChoiceType(OBJECT_TYPES), nullable=False)
    obj_id      = Column(Integer, nullable=False)
    obj_name    = Column(String, nullable=True)

    @classmethod
    def get_comments_list(cls, user, session, id=None):
        query = session.query(cls)

        if not id is None:
            if not isinstance(id, list):
                id = [id]
            query = query.filter(cls.id.in_(id))
        return query