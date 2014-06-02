# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from settings import DATABASE

print DATABASE['postgresql']
engine = create_engine(URL(**DATABASE['postgresql']))

Base = declarative_base()

from users import *
from msgr import *
from contents import *
from chats import *
from scheme import *
from topics import *
from persons import *


# Base.metadata.create_all(engine)
