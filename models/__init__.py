# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from utils.connectors import DBWrapper, db_connect


# Init default connections
engine = db_connect()
db = DBWrapper(engine=engine)

# Init default declarative base `
Base = declarative_base()

# Import models
from users import *
from msgr import *
from contents import *
from chats import *
from scheme import *
from topics import *
from persons import *
from media import *
from topics import *
from cdn import *
from extras import *
from tags import *
from content import *