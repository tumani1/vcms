# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session

from settings import DATABASE, DEBUG


__all__ = ['DBWrapper', 'db_connect']


# Function which create connection to the database
def db_connect(type='postgresql', **kwargs):
    db_settings = DATABASE[type]
    if DEBUG:
        kwargs['echo'] = True
    return create_engine(URL(**db_settings), **kwargs)


# Function which create session marker
def create_session(**kwargs):
    return scoped_session(sessionmaker(**kwargs))()


# Class decorator for to the database
class DBWrapper(object):
    def __init__(self, engine, session):

        self.engine = engine
        self.session = session


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            session = self.session

            try:
                return func(session=session, *args, **kwargs)
            except Exception, e:
                session.rollback()
                raise e
            finally:
                session.close()

        return wrapper
