# coding: utf-8

from sqlalchemy import and_, not_, update

from models.users import UsersValues
from models.scheme import Scheme

from utils import need_authorization

from api.users.users_values import get as users_get
from utils.exceptions import RequestErrorException


@need_authorization
def put(auth_user, session=None, **kwargs):
    query = kwargs['query']
    if 'name' in query:
        name = query['name']
    if 'value' in query:
        value = query['value']
    if 'topic' in query:
        topic = query['topic']
    else:
        topic = None
    if not query['name'] or not query['value']:
        raise RequestErrorException
    shema_val = dict(zip(name, value))
    schemes = session.query(Scheme).filter(and_(Scheme.name.in_(name), Scheme.topic_name == topic)).all()
    user_values = []
    for schema in schemes:
        val = shema_val[schema.name]
        try:
            val = int(val)
            kwargs = {'value_int': val}
        except ValueError:
            if len(val) < 256:
                kwargs = {'value_string': val}
            else:
                kwargs = {'value_text': val}

        user_val_obj = session.query(UsersValues).filter(and_(UsersValues.__getattribute__(UsersValues, kwargs.keys()[0]).isnot(None), UsersValues.user_id == auth_user.id)).first()
        if user_val_obj:
            setattr(user_val_obj, kwargs.keys()[0], kwargs[kwargs.keys()[0]])
        else:
            user_values.append(UsersValues(user_id=auth_user.id, scheme_id=schema.id, **kwargs))

    session.add_all(user_values)
    if session.new or session.dirty:
        session.commit()


@need_authorization
def get(auth_user, session, **kwargs):
    return users_get(user_id=auth_user.id, session=session, **kwargs)
