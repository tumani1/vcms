# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import BYTEA
from models import Base


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(BYTEA, nullable=False)
    active = Column(Boolean, default=False)
    instock = Column(Boolean, default=False)
    added = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    price_old = Column(Float, nullable=False)
    is_digital = Column(Boolean, default=False)
