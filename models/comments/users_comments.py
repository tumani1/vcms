# coding: utf-8
from models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey


class UserComments(Base):
    __tablename__ = 'users_comments'
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    comment_id  = Column(Integer, ForeignKey('comments.id'), nullable=False, index=True)
    liked       = Column(DateTime, nullable=False)