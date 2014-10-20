#coding:utf-8
from models.base import Base
from sqlalchemy import Column, Text


class Sms(Base):
    mes = Column(Text())
