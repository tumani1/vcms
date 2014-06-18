# coding: utf-8
from models import db
from models.users import Users
from utils.exceptions import DoesNotExist

from serializer import mUser


@db
def get(auth_user, id, session=None, **kwargs):
    query = session.query(Users).get(id)
    if not query:
        raise DoesNotExist

    return mUser(instance=query, user=auth_user, session=session).data