# coding: utf-8
from models.users.users import Users
from utils.validation import validate_email, validate_int


def post(auth_user, session, **kwargs):
    query = kwargs['query_params']
    firstname = query.get('firstname', None)
    lastname = query.get('lastname', None)
    email = query.get('email', None)
    pswd1 = query.get('pswd1', None)
    pswd2 = query.get('pswd2', None)

    try:
        email = validate_email(email)
    except Exception, e:
        return {'error': u'Некорректный e-mail!'}

    if pswd1 and pswd2 and pswd1 == pswd2:
        password = pswd1
    else:
        return {'error': u'Пароли не совпадают!'}

    if firstname and lastname:
        user = Users(firstname=firstname, lastname=lastname, email=email, password=password)
        session.add(user)
        session.commit()
    else:
        return {'error': u'Имя и фамилия обязательные поля!'}