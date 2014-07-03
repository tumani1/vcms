# coding: utf-8
from models import Users
from utils.hash_password import verify_password
from models import GlobalToken
from utils.exceptions import NotAuthorizedException


def post(auth_user, session, email, password):

    user = session.query(Users).filter(Users.email==email)

    if verify_password(password, user.password):
        return {'token': GlobalToken.generate_token(user.id, session)}
    else:
        raise NotAuthorizedException
    