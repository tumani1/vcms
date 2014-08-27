# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship, contains_eager
from models import Base
from models.eshop.variants.variants_extras import VariantsExtras
from models.eshop.variants.variants_values import VariantsValues
from models.extras.extras import Extras


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

    variant_extras = relationship('VariantsExtras', backref='variants', cascade='all, delete')
    variant_values = relationship('VariantsValues', backref='variants', cascade='all, delete')

    @classmethod
    def tmpl_for_variants(cls, session):
        query = session.query(cls)

        query = query. \
            outerjoin(VariantsExtras, cls.id == VariantsExtras.variant_id).\
            options(contains_eager(cls.variant_extras))

        query = query. \
            outerjoin(VariantsValues, cls.id == VariantsValues.variant_id).\
            options(contains_eager(cls.variant_values))

        return query

    @classmethod
    def get_variants_by_item_id(cls, session, item_id, **kwargs):
        query = cls.tmpl_for_variants(session)
        query = query.filter(cls.item_id == item_id)
        return query

    @classmethod
    def get_variants_by_id(cls, session, variant_id, **kwargs):
        query = session.query(cls).filter(cls.id == variant_id)
        return query

    @classmethod
    def get_variant_extras(cls, session, variant_id, **kwargs):
        subquery = session.query(VariantsExtras.extras_id).filter(VariantsExtras.variant_id == variant_id).subquery()
        query = session.query(Extras).filter(Extras.id.in_(subquery))
        return query