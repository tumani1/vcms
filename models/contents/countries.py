# coding: utf-8
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from models import Base


class Countries(Base):
    __tablename__ = 'countries'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(256), nullable=False)
    name_orig   = Column(String(256), nullable=False)
    description = Column(Text)

    cities      = relationship('Cities', backref='country')

    def __init__(self, name, name_orig, description=None):
        self.name = name
        self.name_orig = name_orig
        self.description = description

    def __repr__(self):
        return "<Countries([{}] {})>".format(self.id, self.name)

