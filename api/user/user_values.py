from models import db, UsersValues, Scheme
from utils import need_authorization


@db
@need_authorization
def put(user, name, value,topic = None, session=None):
    shema_val = dict(zip(name, value))
    schemes = session.query(Scheme).filter(Scheme.name.in_(name)).all()
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
        user_values.append(UsersValues(user_id=user.id, scheme_id=schema.id, **kwargs))
    session.add_all(user_values)
    if session.new:
        session.commit()