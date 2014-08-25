# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersValues
from models.scheme import Scheme
from models.topics import Topics
from utils.exceptions import RequestErrorException
from api.serializers import mValue


def get(user_id, session, query, **kwargs):
    user = session.query(Users).get(user_id)
    if user is None:
        raise RequestErrorException()

    query = session.query(UsersValues).filter(UsersValues.user_id==user.id)

    if 'id' in query:
        if isinstance(query['id'], int):
            ids = [query['id']]
        else:
            ids = query['id']
        query = query.join(Scheme).filter(Scheme.id.in_(ids))

    if 'name' in query:
        if not isinstance(query['name'], list):
            name = [query['name']]
        else:
            name = query['name']
        query = query.join(Scheme).filter(Scheme.name.in_(name))

    if 'topic' in query:
        query = query.join(Scheme).filter(Scheme.topic_name == query['topic'])

    if 'text' in query:
        query = query.join(Scheme).join(Topics).filter(func.to_tsvector(Topics.description).match(query['text']))

    return mValue(instance=query.all(), session=session).data
