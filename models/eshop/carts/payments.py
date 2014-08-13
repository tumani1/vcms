# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float
from models import Base


class Payments(Base):
    __tablename__ = 'payments'

    id         = Column(Integer, primary_key=True)
    cart_id    = Column(Integer, ForeignKey('carts.id'), nullable=False)
    status     = Column(Integer)
    created    = Column(DateTime)
    payed      = Column(DateTime)
    pay_system = Column(String)
    cost       = Column(Float)
