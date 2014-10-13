# coding: utf-8
from models import Countries, Cities, Users, GlobalToken, SessionToken


def create(session, usuff=1, cisuff=1, couid='RU'):
    country = session.query(Countries).get(couid)
    city = Cities(country=country, region="76", name='Test'+str(cisuff), name_orig='Test'+str(cisuff), time_zone='UTC')
    session.add(city)
    session.commit()
    user = Users(city=city, firstname='Test'+str(usuff), lastname='Test'+str(usuff), password='Test', email='test{}@test.ru'.format(usuff))
    session.add(user)
    session.commit()

    return user


def clear(session):
    session.query(Users).delete()
    session.query(Cities).delete()
    session.commit()
