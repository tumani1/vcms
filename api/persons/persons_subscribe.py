# coding: utf-8

import datetime
from models import db, UsersPersons
from utils import need_authorization

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@need_authorization
@db
def get_subscribe(user, person, session, **kwargs):
    params = {
        'user': user.id,
        'person': person,
        'session': session,
    }

    query = UsersPersons.get_user_person(**params).first()

    if not query is None:
        return query.check_subscribed

    return False


@need_authorization
@db
def post_subscribe(user, person, session, **kwargs):
    params = {
        'user': user.id,
        'person': person,
        'session': session,
    }

    date = datetime.datetime.now()
    up = UsersPersons.get_user_person(**params).first()

    if up is None:
        up = UsersPersons(user_id=user.id, person_id=person, subscribed=date)
        session.add(up)
    else:
        up.subscribed = date

    session.commit()


@need_authorization
@db
def delete_subscribe(user, person, session, **kwargs):
    params = {
        'user': user.id,
        'person': person,
        'session': session,
    }

    # Delete query
    up = UsersPersons.get_user_person(**params).first()
    if not up is None:
        up.subscribed = None
        session.commit()
