# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.dialects.postgresql import BYTEA
from models import Base


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)
    instock = Column(Boolean, default=False)
    added = Column(DateTime, nullable=True)
    price = Column(Float, nullable=True)
    price_old = Column(Float, nullable=True)
    is_digital = Column(Boolean, default=True)

    @classmethod
    def tmpl_for_items(cls, user, session):
        query = session.query(cls)
        return query


    @classmethod
    def get_items_list(cls, user, session, id=None, **kwargs):
        query = cls.tmpl_for_items(user, session)
        if not id is None:
            query = query.filter(cls.id.in_(id))
        return query