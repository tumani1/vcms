# coding: utf-8

from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, ForeignKey
from sqlalchemy_utils import ChoiceType

from models import Base


class Scheme(Base):
    __tablename__ = 'scheme'

    KLASS_TYPE = (
        ('int', 'Int'),
        ('string', 'String'),
        ('text', 'Text'),
    )

    id           = Column(Integer, primary_key=True)
    topic_name   = Column(String, ForeignKey('topics.name'), nullable=True)
    klass        = Column(ChoiceType(KLASS_TYPE), nullable=False, default='int')
    name         = Column(String, nullable=False)
    type         = Column(String, nullable=False, default='')
    access_level = Column(SmallInteger, nullable=False, default=0)
    status       = Column(SmallInteger, nullable=False, default=0)
    internal     = Column(Boolean, nullable=False, default=0)
