# coding: utf-8
from models.users import Users
from models.tokens import GlobalToken
from models.users.constants import APP_USER_LOGIN_FIELD_PHONE, APP_USER_LOGIN_FIELD_EMAIL
from utils.exceptions import NotAuthorizedException
import re


def post(auth_user, session, **kwargs):
    qp = kwargs.get('query_params')
    login = str(qp.get('login'))
    password = qp.get('password')
    login_field = APP_USER_LOGIN_FIELD_EMAIL
    if not re.search(ur'@', login):
        login_field = APP_USER_LOGIN_FIELD_PHONE
        login = '+' + login.strip()

    user = session.query(Users).filter(getattr(Users, login_field) == login).first()
    if not user:
        raise NotAuthorizedException
    else:
        if user.password == str(password):
            return {'token': GlobalToken.generate_token(user.id, session)}
        else:
            raise NotAuthorizedException