# coding: utf-8
from models import Countries, Cities, Users, GlobalToken, SessionToken


def create(session):
    country = session.query(Countries).get('RU')
    session.add(country)
    session.commit()

    city = Cities(country=country, name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()

    user = Users(city=city, firstname="Test", lastname="Test", password='Test', email='test1@test.ru')
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
