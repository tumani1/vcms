# coding: utf-8
import datetime

from models.mongo import Stream, constant
from models.persons import UsersPersons

from utils import need_authorization
from utils.validation import validate_int

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@need_authorization
def get_subscribe(person_id, auth_user, session, **kwargs):
    # Validation person value
    person_id = validate_int(person_id, min_value=1)

    params = {
        'user': auth_user,
        'person_id': person_id,
        'session': session,
    }

    query = UsersPersons.get_user_person(**params).first()

    if not query is None:
        return {'subscribed': query.check_subscribed}

    return {'subscribed': False}


@need_authorization
def post_subscribe(person_id, auth_user, session, **kwargs):
    # Validation person value
    person_id = validate_int(person_id, min_value=1)

    params = {
        'user': auth_user,
        'person_id': person_id,
        'session': session,
    }

    date = datetime.datetime.utcnow()
    up = UsersPersons.get_user_person(**params).first()

    if up is None:
        up = UsersPersons(user_id=auth_user.id, person_id=person_id, subscribed=date)
        session.add(up)
    else:
        up.subscribed = date

    session.commit()
    Stream.signal(type_=constant.APP_STREAM_TYPE_PERS_S, object={'person_id': person_id}, user_id=auth_user.id)


@need_authorization
def delete_subscribe(person_id, auth_user, session, **kwargs):
    # Validation person value
    person_id = validate_int(person_id, min_value=1)

    params = {
        'user': auth_user,
        'person_id': person_id,
        'session': session,
    }

    # Delete query
    up = UsersPersons.get_user_person(**params).first()
    if not up is None:
        up.subscribed = None
        session.commit()
