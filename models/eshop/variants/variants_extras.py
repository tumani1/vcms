# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from models import Base


class VariantsExtras(Base):
    __tablename__ = 'variants_extras'

    id = Column(Integer, primary_key=True)
    variant_id = Column(ForeignKey('variants.id'), nullable=False)
    extras_id = Column(ForeignKey('extras.id'), nullable=False)
    extras_type = Column(Integer, nullable=True)
