# coding: utf-8

import os
import sqlalchemy

import settings
from models import Base
from utils.connectors import db_connect

def setup_package():
    engine = db_connect(type="postgresql")
    engine.execute("drop schema public cascade; create schema public;")

    # engine = sqlalchemy.create_engine("postgresql+psycopg2://pgadmin:qwerty@/postgres").connect() #pgadmin:qwerty@localhost:5432/
    # engine.execute("DROP DATABASE IF EXISTS {0};".format(db_name))
    # engine.execute("CREATE DATABASE {0};".format(db_name))
    # engine.execute("USE {0};".format(db_name))

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture


def teardown_package():
    os.environ['TEST_EXEC'] = '0'

    engine = db_connect(type="postgresql")
    engine.execute("drop schema public cascade; create schema public;")