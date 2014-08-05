# coding: utf-8
from models.users import Users
from utils.exceptions import RequestErrorException

from api.serializers import mUser


def get(user_id, auth_user, session, **kwargs):
    query = session.query(Users).get(user_id)
    if not query:
        raise RequestErrorException

    return mUser(instance=query, user=auth_user, session=session).data
