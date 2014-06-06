from models import db , Countries,Cities,Users

@db
def create_test_user(session = None):

    country = Countries(name = 'Test', nome_orig ="Test")
    session.add(country)
    session.commit()
    city = Cities(name="Test",name_orig = "Test", country=country)
    session.add(city)
    session.commit()

    user = Users(firstname="Test", lastname="Test",password = "Test")
    session.add(user)
    session.commit()
