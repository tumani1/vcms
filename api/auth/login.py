# coding: utf-8
from models.users import Users
from models.tokens import GlobalToken
from utils.exceptions import NotAuthorizedException, RequestErrorException
from utils.validation import validate_phone_number
import re


def post(auth_user, session, **kwargs):
    qp = kwargs.get('query_params')
    login = qp.get('login')
    password = qp.get('password')

    if login and password:
            if re.search(ur'@', login):
                user = session.query(Users).filter(Users.email == login).first()
            else:
                login = '+' + validate_phone_number(login)
                user = session.query(Users).filter(Users.phone == login).first()

            if user:
                if user.password == password:
                    return {'token': GlobalToken.generate_token(user.id, session)}
                else:
                    raise NotAuthorizedException
            raise NotAuthorizedException
    else:
        raise RequestErrorException