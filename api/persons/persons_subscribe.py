# coding: utf-8

import datetime

from models.persons import UsersPersons

from utils import need_authorization
from utils.validation import validate_int

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@need_authorization
def get_subscribe(auth_user, id, session, **kwargs):
    # Validation person value
    person = validate_int(id, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    params = {
        'user': auth_user,
        'person_id': person,
        'session': session,
    }

    query = UsersPersons.get_user_person(**params).first()

    if not query is None:
        return {'subscribed': query.check_subscribed}

    return {'subscribed': False}


@need_authorization
def post_subscribe(auth_user, id, session, **kwargs):
    # Validation person value
    person = validate_int(id, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    params = {
        'user': auth_user,
        'person_id': person,
        'session': session,
    }

    date = datetime.datetime.utcnow()
    up = UsersPersons.get_user_person(**params).first()

    if up is None:
        up = UsersPersons(user_id=auth_user.id, person_id=person, subscribed=date)
        session.add(up)
    else:
        up.subscribed = date

    session.commit()


@need_authorization
def delete_subscribe(auth_user, id, session, **kwargs):
    # Validation person value
    person = validate_int(id, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    params = {
        'user': auth_user,
        'person_id': person,
        'session': session,
    }

    # Delete query
    up = UsersPersons.get_user_person(**params).first()
    if not up is None:
        up.subscribed = None
        session.commit()
