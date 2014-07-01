# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersValues
from models.scheme import Scheme
from models.topics import Topics
from utils.exceptions import RequestErrorException
from serializer import mValue


def get(user, session, name=None, topic=None, text=None, id=None, **kwargs):
    user = session.query(Users).get(user)
    if user is None:
        raise RequestErrorException

    query = session.query(UsersValues).filter(UsersValues.user_id==user.id)

    if not id is None:
        if isinstance(id, int):
            id = [id]
        query = query.join(Scheme).filter(Scheme.id.in_(id))

    if not name is None:
        if not isinstance(name, list):
            name = [name]
        query = query.join(Scheme).filter(Scheme.name.in_(name))

    if not topic is None:
        query = query.join(Scheme).filter(Scheme.topic_name == topic)

    if not text is None:
        query = query.join(Scheme).join(Topics).filter(func.to_tsvector(Topics.description).match(text))

    return mValue(instance=query.all(), session=session).data
