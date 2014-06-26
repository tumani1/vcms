from models import UsersValues, Scheme
from db_engine import db
from utils import need_authorization
from sqlalchemy import and_, not_, update
from api.users.users_values import get as users_get

@db
@need_authorization
def put(auth_user, name, value, topic=None, session=None):
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
def get(auth_user, **kwargs):
        users_get(auth_user.id, **kwargs)