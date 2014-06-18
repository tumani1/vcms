# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from utils.connectors import DBWrapper, db_connect, create_session


# Init default connections
engine = db_connect()

# Init Session
session = create_session(bind=engine, expire_on_commit=False)

db = DBWrapper(engine=engine, session=session)

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
from tokens import *
