# coding: utf-8
from models import Countries, Cities, Users
from utils import hash_password


def create(session):
    country = Countries(name='Test', name_orig="Test")
    session.add(country)
    session.commit()

    city = Cities(country=country, name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()

    user = Users(city=city, firstname="Test", lastname="Test", password=hash_password.hash_pass('Test'))
    session.add(user)
    session.commit()

    return user.id
