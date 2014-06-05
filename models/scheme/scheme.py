# coding: utf-8

from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models import Base


class Scheme(Base):
    __tablename__ = 'scheme'

    M_SCHEME_INT = u'int'
    M_SCHEME_STR = u'string'
    M_SCHEME_TXT = u'text'

    KLASS_TYPE = (
        (M_SCHEME_INT, u'Целое'),
        (M_SCHEME_STR, u'Строка'),
        (M_SCHEME_TXT, u'Текст'),
    )

    id           = Column(Integer, primary_key=True)
    topic_name   = Column(String, ForeignKey('topics.name'), nullable=True)
    klass        = Column(ChoiceType(KLASS_TYPE), nullable=False, default=M_SCHEME_INT, index=True)
    name         = Column(String, nullable=False)
    type         = Column(String, nullable=False, default='')
    access_level = Column(SmallInteger, nullable=False, default=0)
    status       = Column(SmallInteger, nullable=False, default=0)
    internal     = Column(Boolean, nullable=False, default=0)