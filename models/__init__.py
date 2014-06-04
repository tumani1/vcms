# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from connectors import DBWrapper

db = DBWrapper()
Base = declarative_base()

from users import *
from msgr import *
from contents import *
from chats import *
from scheme import *
from topics import *
from persons import *
