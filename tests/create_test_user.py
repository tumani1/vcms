from models import db, Countries, Cities, Users


@db
def create(session = None):

    country = Countries(name='Test', name_orig="Test")
    session.add(country)
    session.commit()
    city = Cities(country=country, name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()
    user = Users(city=city, firstname="Test", lastname="Test", password="Test")
    session.add(user)
    session.commit()