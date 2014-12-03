# coding: utf-8
from models import Users


def create(session, usuff=1):
    user = Users(firstname='Test'+str(usuff), lastname='Test'+str(usuff), password='Test', email='test{}@test.ru'.format(usuff))
    session.add(user)
    session.commit()
    return user


def clear(session):
    for user in session.query(Users).all():
        session.delete(user)
    session.commit()
