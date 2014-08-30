# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersValues
from models.scheme import Scheme
from models.topics import Topics
from utils.exceptions import RequestErrorException
from api.serializers import mValue


def get(user_id, session, **kwargs):
    user = session.query(Users).get(user_id)
    if user is None:
        raise RequestErrorException()

    query = session.query(UsersValues).filter(UsersValues.user_id==user.id)

    if 'id' in kwargs['query_params']:
        if isinstance(kwargs['query_params']['id'], int):
            ids = [kwargs['query_params']['id']]
        else:
            ids = kwargs['query_params']['id']
        query = query.join(Scheme).filter(Scheme.id.in_(ids))

    if 'name' in kwargs['query_params']:
        if not isinstance(kwargs['query_params']['name'], list):
            name = [kwargs['query_params']['name']]
        else:
            name = kwargs['query_params']['name']
        query = query.join(Scheme).filter(Scheme.name.in_(name))

    if 'topic' in kwargs['query_params']:
        query = query.join(Scheme).filter(Scheme.topic_name == kwargs['query_params']['topic'])

    if 'text' in kwargs['query_params']:
        query = query.join(Scheme).join(Topics).filter(func.to_tsvector(Topics.description).match(kwargs['query_params']['text']))

    return mValue(instance=query.all(), session=session).data
