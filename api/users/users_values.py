# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersValues
from models.scheme import Scheme
from models.topics import Topics
from utils.exceptions import RequestErrorException
from api.serializers import mValue


def get(id, session, **kwargs):
    user = session.query(Users).get(id)
    if user is None:
        raise RequestErrorException()

    query = session.query(UsersValues).filter(UsersValues.user_id==user.id)

    if 'id' in kwargs['query']:
        if isinstance(kwargs['query']['id'], int):
            ids = [kwargs['query']['id']]
        else:
            ids = kwargs['query']['id']
        query = query.join(Scheme).filter(Scheme.id.in_(ids))

    if 'name' in kwargs['query']:
        if not isinstance(kwargs['query']['name'], list):
            name = [kwargs['query']['name']]
        else:
            name = kwargs['query']['name']
        query = query.join(Scheme).filter(Scheme.name.in_(name))

    if 'topic' in kwargs['query']:
        query = query.join(Scheme).filter(Scheme.topic_name == kwargs['query']['topic'])

    if 'text' in kwargs['query']:
        query = query.join(Scheme).join(Topics).filter(func.to_tsvector(Topics.description).match(kwargs['query']['text']))

    return mValue(instance=query.all(), session=session).data
