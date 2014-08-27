# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from models import Base


class CartLog(Base):
    __tablename__ = 'cart_log'

    id         = Column(Integer, primary_key=True)
    cart_id    = Column(Integer, ForeignKey('carts.id'), nullable=False)
    status     = Column(Integer)
    time       = Column(DateTime, nullable=True)
    comment    = Column(String)

    @classmethod
    def get_cart_log_by_cart_id(cls, session, carts_id):
        query = session.query(cls).filter(cls.cart_id == carts_id)
        return query
