# coding: utf-8
from models.users.users import Users
from utils.validation import validate_email, validate_int


def post(auth_user, session, **kwargs):
    query = kwargs['query']
    if 'firstname' in query:
        firstname = query['firstname']
    else:
        raise Exception(u"Empty name")
    if 'lastname' in query:
        lastname = query['lastname']
    else:
        raise Exception(u"Empty name")
    if 'email' in query:
        email = query['email']
    else:
        raise Exception(u"Empty name")
    if 'pswd1' in query:
        pswd1 = query['pswd1']
    else:
        raise Exception(u"Empty name")
    if 'pswd2' in query:
        pswd2 = query['pswd2']
    else:
        raise Exception(u"Empty name")
    if 'city_id' in query:
        city_id = query['city_id']
    else:
        raise Exception(u"Empty name")
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
