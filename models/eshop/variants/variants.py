# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship, contains_eager
from models import Base
from models.eshop.variants.variants_extras import VariantsExtras


class Variants(Base):
    __tablename__ = 'variants'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    name = Column(String, nullable=True)
    description = Column(BYTEA, nullable=True)
    price = Column(Float, nullable=True)
    price_old = Column(Float, nullable=True)
    active = Column(Boolean, default=False)
    stock_cnt = Column(Integer, nullable=True)
    reserved_cnt = Column(Integer, nullable=True)
    added = Column(DateTime, nullable=True)

    variant_extras = relationship('VariantsExtras', backref='items', cascade='all, delete')

    @classmethod
    def tmpl_for_variants(cls, user, session):
        query = session.query(cls)

        query = query. \
            outerjoin(VariantsExtras, cls.id == VariantsExtras.variant_id).\
            options(contains_eager(cls.variant_extras))

        return query

    @classmethod
    def get_variants_by_item_id(cls, user, session, item_id, **kwargs):
        query = cls.tmpl_for_variants(user, session)
        query = query.filter(cls.item_id == item_id)
        return query