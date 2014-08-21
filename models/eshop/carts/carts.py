# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from models import Base


class Carts(Base):
    __tablename__ = 'carts'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    items_cnt  = Column(Integer)
    status     = Column(Integer)
    cost_total = Column(Float)
    crated     = Column(DateTime)
    updated    = Column(DateTime)


    @classmethod
    def get_cart_by_user_id(cls, session, user_id, **kwargs):
        query = session.query(cls).filter(cls.user_id == user_id)
        return query