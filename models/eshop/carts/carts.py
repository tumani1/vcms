# coding: utf-8
import datetime
from models import Base
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship


class Carts(Base):
    __tablename__ = 'carts'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    items_cnt  = Column(Integer)
    status     = Column(String)
    cost_total = Column(Float)
    created     = Column(DateTime, default=datetime.datetime.utcnow)
    updated    = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    payments = relationship("Payments", backref='cart')

    @classmethod
    def get_cart_by_user_id(cls, session, user_id, **kwargs):
        query = session.query(cls).filter(cls.user_id == user_id)
        return query

    def __repr__(self):
        return u"<Carts(id={}, user_id={}, items_cnt={})>".format(self.id, self.user_id, self.items_cnt)