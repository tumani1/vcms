# coding: utf-8
from models.users.users import Users
from utils.validation import validate_email, validate_int


def post(auth_user, session, firstname, lastname, email, pswd1, pswd2, city_id, **kwargs):
    try:
        email = validate_email(email)
    except Exception, e:
        return {'error': u'Некорректный e-mail!'}
    city_id = validate_int(city_id, min_value=1)
    if pswd1 and pswd2 and pswd1 == pswd2:
        password = pswd1
    else:
        return {'error': u'Пароли не совпадают!'}
    if firstname and lastname:
        user = Users(firstname=firstname, lastname=lastname, email=email, city_id=city_id, password=password)
        session.add(user)
        session.commit()
    else:
        return {'error': u'Имя и фамилия обязательные поля!'}
