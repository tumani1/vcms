# coding: utf-8
import datetime
from models import Base
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, and_
from sqlalchemy.orm import relationship, contains_eager
from models import Base, ItemsCarts, Payments, ItemsExtras, ItemsObjects, UsersItems, CartLog


class Carts(Base):
    __tablename__ = 'carts'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    items_cnt  = Column(Integer)
    status     = Column(String)
    cost_total = Column(Float)
    created     = Column(DateTime, default=datetime.datetime.utcnow)
    updated    = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    items_carts = relationship('ItemsCarts', backref='carts', cascade='all, delete')
    payments = relationship('Payments', backref='carts', cascade='all, delete')
    log = relationship('CartLOg', backref='carts', cascade='all, delete')

    @classmethod
    def tmpl_for_carts(cls, carts_id, session, user):

        query = session.query(cls).filter(cls.id == carts_id)

        query = query. \
            outerjoin(ItemsCarts, carts_id == ItemsCarts.carts_id).\
            options(contains_eager(cls.carts_items_carts))

        query = query. \
            outerjoin(Payments, carts_id == Payments.cart_id).\
            options(contains_eager(cls.payments))

        query = query. \
            outerjoin(CartLog, carts_id == CartLog.cart_id).\
            options(contains_eager(cls.log))

        return query

    @classmethod
    def get_cart_by_user_id(cls, session, user_id, **kwargs):
        query = session.query(cls).filter(cls.user_id == user_id)
        return query

    def __repr__(self):
        return u"<Carts(id={}, user_id={}, items_cnt={})>".format(self.id, self.user_id, self.items_cnt)