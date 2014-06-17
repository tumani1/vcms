# coding: utf-8

import datetime

from models import db, UsersPersons

from utils import need_authorization
from utils.validation import validate_int

__all__ = ['get_like', 'post_like', 'delete_like']


@need_authorization
@db
def get_like(user, person, session, **kwargs):
    # Validation person value
    person = validate_int(person, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    params = {
        'user': user.id,
        'person': person,
        'session': session,
    }

    query = UsersPersons.get_user_person(**params).first()

    if not query is None:
        return {'liked': query.check_liked}

    return {'liked': 0}


@need_authorization
@db
def post_like(user, person, session, **kwargs):
    # Validation person value
    person = validate_int(person, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    params = {
        'user': user.id,
        'person': person,
        'session': session,
    }

    date = datetime.datetime.utcnow()

    up = UsersPersons.get_user_person(**params).first()

    if up is None:
        up = UsersPersons(user_id=user.id, person_id=person, liked=date)
        session.add(up)
    else:
        up.liked = date

    session.commit()


@need_authorization
@db
def delete_like(user, person, session, **kwargs):
    # Validation person value
    person = validate_int(person, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    params = {
        'user': user.id,
        'person': person,
        'session': session,
    }

    # Delete query
    up = UsersPersons.get_user_person(**params).first()
    if not up is None:
        up.liked = None
        session.commit()
