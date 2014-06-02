# coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from settings import ENGINE_STR


engine = create_engine(ENGINE_STR)

Base = declarative_base()

from users import *
from msgr import *
from contents import *
from chats import *

Base.metadata.create_all(engine)