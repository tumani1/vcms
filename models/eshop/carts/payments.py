# coding: utf-8
import datetime
from models import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float


class Payments(Base):
    __tablename__ = 'payments'

    id         = Column(Integer, primary_key=True)
    cart_id    = Column(Integer, ForeignKey('carts.id'), nullable=False)
    status     = Column(String)
    created    = Column(DateTime, default=datetime.datetime.utcnow)
    payed      = Column(DateTime)
    pay_system = Column(String)
    cost       = Column(Float)

    def __repr__(self):
        return u"<Payments(id={}, cart_id={}, cost={})>".format(self.id, self.cart_id, self.cost)