# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from models import Base


class CartLog(Base):
    __tablename__ = 'cart_log'

    id         = Column(Integer, primary_key=True)
    cart_id    = Column(Integer, ForeignKey('carts.id'), nullable=False)
    status     = Column(Integer)
    time       = Column(DateTime)
    comment    = Column(String)
