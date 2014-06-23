# coding: utf-8

import datetime

from models import UsersTopics
from db_engine import db
from utils import need_authorization

__all__ = ['get_like', 'post_like', 'delete_like']


@need_authorization
@db
def get_like(auth_user, name, session, **kwargs):
    params = {
        'user': auth_user,
        'name': name,
        'session': session,
    }

    query = UsersTopics.get_user_topic(**params).first()
    if not query is None:
        return {'liked': query.check_liked}

    return {'liked': 0}


@need_authorization
@db
def post_like(auth_user, name, session, **kwargs):
    params = {
        'user': auth_user,
        'name': name,
        'session': session,
    }

    date = datetime.datetime.utcnow()

    ut = UsersTopics.get_user_topic(**params).first()

    if ut is None:
        ut = UsersTopics(user_id=auth_user.id, topic_name=name, liked=date)
        session.add(ut)
    else:
        ut.liked = date

    session.commit()


@need_authorization
@db
def delete_like(auth_user, name, session, **kwargs):
    params = {
        'user': auth_user,
        'name': name,
        'session': session,
    }

    # Delete query
    ut = UsersTopics.get_user_topic(**params).first()
    if not ut is None:
        ut.liked = None
        session.commit()
