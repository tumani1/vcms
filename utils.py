# coding: utf-8

from models import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
