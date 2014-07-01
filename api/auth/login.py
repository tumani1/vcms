# coding: utf-8
from models import Users
from utils.hash_password import verify_password
from models import GlobalToken
from utils.exceptions import NotAuthorizedException


def post(user_id, email, password, session=None):

    user = session.query(Users).filter(email=email)

    if verify_password(password, user.password):
        return {'token': GlobalToken.generate_token(user_id, session)}
    else:
        raise NotAuthorizedException
    