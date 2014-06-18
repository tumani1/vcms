import datetime

from models import db, Countries, Cities, Users, Topics


@db
def create(session=None):

    country = Countries(name='Test', name_orig="Test")
    session.add(country)
    session.commit()
    city = Cities(country=country, name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()
    user = Users(city=city, firstname="Test", lastname="Test", password="Test")
    session.add(user)
    session.commit()

@db
def create_topic(session):
    topic = Topics(name="test11", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status='a', type='news')
    session.add(topic)
    session.commit()

