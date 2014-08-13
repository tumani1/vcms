# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import BYTEA
from models import Base


class Variants(Base):
    __tablename__ = 'variants'
    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('item.id'), nullable=False)
    name = Column(String, nullable=True)
    description = Column(BYTEA, nullable=True)
    price = Column(Float, nullable=True)
    price_old = Column(Float, nullable=True)
    active = Column(Boolean, default=False)
    stock_int = Column(Integer, nullable=True)



