# coding: utf-8
from settings import DEBUG, DATABASE
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session


__all__ = ['DBWrapper', 'db_connect']


def db_connect(type='postgresql', **kwargs):
    db_settings = DATABASE[type]

    if DEBUG:
        kwargs['echo'] = True

    return create_engine(URL(**db_settings), **kwargs)


def create_session(**kwargs):
    return scoped_session(sessionmaker(**kwargs))()


class DBW(object):
    """Декоратор-синглтон , который используется при определении методов API.
     Передает им в параметр session уже существующий объект сессии"""

    class __DBW(object):

        def __init__(self):
            self.engine = db_connect()
            self.session = create_session(bind=self.engine, expire_on_commit=False)

        def __call__(self, func):
            def wrapper(*args, **kwargs):
                try:
                    return func(session=self.session, *args, **kwargs)
                except Exception, e:
                    self.session.rollback()
                    raise e
                finally:
                    self.session.close()

            return wrapper

    instance = None

    def __init__(self):
        if not DBW.instance:
            DBW.instance = DBW.__DBW()

    def __call__(self, func):
        return self.instance.__call__(func)

DBWrapper = DBW()