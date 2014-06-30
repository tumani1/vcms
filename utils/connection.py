# coding: utf-8
from settings import DEBUG, DATABASE
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session


def db_connect(type='postgresql', **kwargs):
    db_settings = DATABASE[type]

    if DEBUG:
        kwargs['echo'] = True

    return create_engine(URL(**db_settings), **kwargs)


def create_session(**kwargs):
    return scoped_session(sessionmaker(**kwargs))()


def get_session(**kwargs):
    engine = db_connect()
    return create_session(bind=engine, expire_on_commit=False)