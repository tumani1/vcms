# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, String
from models import Base


class VariantsValues(Base):
    __tablename__ = 'variants_values'

    id = Column(Integer, primary_key=True)
    scheme_id = Column(ForeignKey('variants_scheme.id'), nullable=False)
    variant_id = Column(ForeignKey('variants.id'), nullable=False)
    name = Column(String, nullable=True)
    value = Column(String, nullable=True)
