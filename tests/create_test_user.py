# coding: utf-8
from models import Countries, Cities, Users, GlobalToken


def create(session):
    country = Countries(name='Test', name_orig="Test")
    session.add(country)
    session.commit()

    city = Cities(country=country, name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()

    user = Users(city=city, firstname="Test", lastname="Test", password='Test')
    session.add(user)
    session.commit()

    return user


def clear(session):
    session.query(Countries).delete()
    session.query(Cities).delete()
    session.query(GlobalToken).delete()
    session.query(Users).delete()
    session.commit()
