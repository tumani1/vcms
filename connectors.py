from sqlalchemy import create_engine, pool
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from settings import DATABASE


__all__ = ['DBWrapper', 'db_connect']


# Create connection to the database
def db_connect(type='postgresql', **kwargs):
    db_settings = DATABASE[type]
    return create_engine(URL(**db_settings), **kwargs)


class DBWrapper(object):
    def __init__(self, engine=None, poolclass=None):
        poolclass = poolclass or pool.SingletonThreadPool

        if engine is None:
            self.engine = db_connect(poolclass=poolclass)
        else:
            self.engine = create_engine(engine, poolclass=poolclass)


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            session = sessionmaker(bind=self.engine, expire_on_commit=False)()
            try:
                return func(session=session, *args, **kwargs)
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        return wrapper
