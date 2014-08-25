# coding: utf-8
from models.users.users import Users
from utils.validation import validate_email, validate_int
from utils.exceptions import RequestErrorException


def post(auth_user, session, **kwargs):
    query = kwargs['query']
    firstname = query.get('firstname', None)

    if 'firstname' in query:
        firstname = query['firstname']
    else:
        raise RequestErrorException

    if 'lastname' in query:
        lastname = query['lastname']
    else:
        raise RequestErrorException

    if 'email' in query:
        email = query['email']
    else:
        raise RequestErrorException

    if 'pswd1' in query:
        pswd1 = query['pswd1']
    else:
        raise RequestErrorException

    if 'pswd2' in query:
        pswd2 = query['pswd2']
    else:
        raise RequestErrorException

    if 'city_id' in query:
        city_id = query['city_id']
    else:
        raise RequestErrorException

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
