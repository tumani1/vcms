# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersValues
from models.scheme import Scheme
from models.topics import Topics
from utils.exceptions import RequestErrorException
from serializer import mValue


def get(user_id, session, **kwargs):
    user = session.query(Users).get(user_id)
    if user is None:
        raise RequestErrorException()

    query = session.query(UsersValues).filter(UsersValues.user_id==user.id)

    if 'id' in kwargs:
        if isinstance(kwargs['id'], int):
            ids = [kwargs['id']]
        else:
            ids = kwargs['id']
        query = query.join(Scheme).filter(Scheme.id.in_(ids))

    if 'name' in kwargs:
        if not isinstance(kwargs['name'], list):
            name = [kwargs['name']]
        else:
            name = kwargs['name']
        query = query.join(Scheme).filter(Scheme.name.in_(name))

    if 'topic' in kwargs:
        query = query.join(Scheme).filter(Scheme.topic_name == kwargs['topic'])

    if 'text' in kwargs:
        query = query.join(Scheme).join(Topics).filter(func.to_tsvector(Topics.description).match(kwargs['text']))

    return mValue(instance=query.all(), session=session).data
