# coding: utf-8

from models import Base
from connectors import db_connect


if __name__ == '__main__':
    Base.metadata.create_all(bind=db_connect())
