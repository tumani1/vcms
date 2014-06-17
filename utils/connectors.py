# coding: utf-8

from sqlalchemy import create_engine, pool
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


# Class decorator for to the database
class DBWrapper(object):
    def __init__(self, engine=None, poolclass=None):
        poolclass = poolclass or pool.SingletonThreadPool

        if engine is None:
            self.engine = db_connect(poolclass=poolclass)
        else:
            self.engine = engine


    def __call__(self, func):
        def wrapper(*args,**kwargs):
            # Init params
            params = {
                'bind': self.engine,
                'expire_on_commit': False,
            }

            # Init Session
            session = scoped_session(sessionmaker(**params))()

            try:
                return func(session=session, *args, **kwargs)
            except Exception, e:
                session.rollback()
                raise e
            finally:
                session.close()

        return wrapper
