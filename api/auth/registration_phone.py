# coding: utf-8
from random import choice
from string import digits, ascii_letters
from datetime import date, timedelta
from phonenumbers import parse
from models.users.users import Users
from utils.smsc_api import SMSC
from utils.exceptions import RequestErrorException, NotAllowed


LOGIN = 'solarispromo'
PASSWORD = '40cbe6860ee7014fdc2d9f5800c6dc70'
MAX_ATTEMPTS = 3


def post(session, auth_user, **kwargs):
    query = kwargs.get('query_params')
    phone_number = query.get('phone_number', '')
    phone_number = '+' + phone_number.strip()

    try:
        # методом parse отлавливаем некоторые виды исключений, связанных с номерами телефонов
        pn = parse(phone_number)
        smsc = SMSC(login=LOGIN, password=PASSWORD)
        random_password = ''.join((choice(ascii_letters+digits) for _ in range(8)))
        message = 'Ваш пароль для входа: '+random_password

        filtered = session.query(Users).filter(Users.phone == phone_number)
        if not session.query(filtered.exists()).scalar():
            user = Users(phone=phone_number, firstname=phone_number, lastname=phone_number, password=random_password, attempts_count=1)
            session.add(user)
            session.commit()
            smsc.send_sms(phone_number, message)
        else:
            u = filtered.first()
            if u.attempts_count < MAX_ATTEMPTS:
                isallowed = date.today() > u.deny_to if u.deny_to else True  # deny_to может быть None
                if isallowed:
                    u.password = random_password
                    u.attempts_count += 1
                    session.add(u)
                    session.commit()
                    smsc.send_sms(phone_number, message)
                else:
                    raise NotAllowed
            else:
                u.deny_to = date.today() + timedelta(days=14)
                u.attempts_count = 0
                session.add(u)
                session.commit()
                raise NotAllowed

    except NotAllowed:
        raise NotAllowed

    except Exception:
        raise RequestErrorException