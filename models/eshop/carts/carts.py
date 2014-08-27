# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, and_
from sqlalchemy.orm import relationship, contains_eager
from models import Base, ItemsCarts, Payments, ItemsExtras, ItemsObjects, UsersItems, CartLog


class Carts(Base):
    __tablename__ = 'carts'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    items_cnt  = Column(Integer, nullable=True)
    status     = Column(Integer, nullable=True)
    cost_total = Column(Float, nullable=True)
    crated     = Column(DateTime, nullable=True)
    updated    = Column(DateTime, nullable=True)

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

