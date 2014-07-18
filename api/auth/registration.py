# coding: utf-8
from models.users.users import Users
from utils.validation import validate_email, validate_int


def post(session, firstname, lastname, email, pswd1, pswd2, city_id, **kwargs):
    try:
        email = validate_email(email)
        city = validate_int(city_id, min_value=1)
        if pswd1 and pswd2 and pswd1 == pswd2:
            password = pswd1
        else:
            raise Exception(u"Пароли не совпадают!")
        if firstname and lastname:
            user = Users(firstname=firstname, lastname=lastname, email=email, city_id=city, password=password)
            session.add(user)
            session.commit()
        else:
            raise Exception(u"Имя и фамилия обязательные поля!")
    except Exception, e:
        print e.message
