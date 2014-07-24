# coding: utf-8
from models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, and_


class UsersComments(Base):
    __tablename__ = 'users_comments'
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    comment_id  = Column(Integer, ForeignKey('comments.id'), nullable=False, index=True)
    liked       = Column(DateTime, nullable=True)

    @classmethod
    def get_user_comments(cls, user, session, id, **kwargs):
        query = session.query(cls).filter(and_(cls.comment_id == id, cls.user_id == user)).first()
        return query