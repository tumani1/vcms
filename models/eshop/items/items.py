# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import BYTEA
from models import Base


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(BYTEA, nullable=True)
    active = Column(Boolean, default=False)
    instock = Column(Boolean, default=False)
    added = Column(DateTime, nullable=True)
    price = Column(Float, nullable=True)
    price_old = Column(Float, nullable=True)
    is_digital = Column(Boolean, default=True)
