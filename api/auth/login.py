# coding: utf-8

from models import GlobalToken, Users
from utils.exceptions import NotAuthorizedException


def post(auth_user, session, email, password, **kwargs):
    user = session.query(Users).filter(Users.email == email).first()

    if user.password == str(password):
        return {'token': GlobalToken.generate_token(user.id, session)}
    else:
        raise NotAuthorizedException
