# coding: utf-8
from models.users import Users
from utils.exceptions import DoesNotExist

from api.serializers import mUser


def get(user_id, auth_user, session, **kwargs):
    query = session.query(Users).get(user_id)
    if not query:
        raise DoesNotExist

    return mUser(instance=query, user=auth_user, session=session).data
