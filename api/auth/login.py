# coding: utf-8

from models.users import Users
from models.tokens import GlobalToken
from utils.exceptions import NotAuthorizedException


def post(auth_user, session, **kwargs):
    email = kwargs['query']['email']
    password = kwargs['query']['password']
    user = session.query(Users).filter(Users.email == email).first()

    if user.password == str(password):
        return {'token': GlobalToken.generate_token(user.id, session)}
    else:
        raise NotAuthorizedException
