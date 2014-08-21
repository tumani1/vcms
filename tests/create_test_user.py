# coding: utf-8
from models import Countries, Cities, Users, GlobalToken, SessionToken


def create(session, usuff=1, cisuff=1):
    country = session.query(Countries).get('RU')
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
    session.commit()
