# coding: utf-8
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from models.base import Base


class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = {'extend_existing': True}

    id          = Column(Integer, primary_key=True)
    name        = Column(String(256), unique=True, nullable=False)
    name_orig   = Column(String(256), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return u"<Countries(id={0}, name={1})>".format(self.id, self.name)

