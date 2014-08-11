# coding: utf-8
from models import Countries, Cities, Users, GlobalToken, SessionToken


def create(session, usuff=1, cisuff=1, cousuff=1):
    country = Countries(name='Test'+str(cousuff), name_orig='Test'+str(cousuff))
    session.add(country)
    session.commit()

    city = Cities(country=country, name='Test'+str(cisuff), name_orig='Test'+str(cisuff), time_zone='UTC')
    session.add(city)
    session.commit()

    user = Users(city=city, firstname='Test'+str(usuff), lastname='Test'+str(usuff), password='Test', email='test{}@test.ru'.format(usuff))
    session.add(user)
    session.commit()

    return user


def clear(session):

    session.query(GlobalToken).delete()
    session.commit()
    session.query(SessionToken).delete()
    session.query(Users).delete()
    session.query(Cities).delete()
    session.query(Countries).delete()
    session.commit()