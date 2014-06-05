# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from connectors import DBWrapper, db_connect

engine = db_connect()
dbWrap = DBWrapper(engine=engine)
Base = declarative_base()

from users import *
from msgr import *
from contents import *
from chats import *
from scheme import *
from persons import *
from topics import *
from media import *
from extras import *
