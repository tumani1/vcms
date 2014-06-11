# coding: utf-8

import datetime

from models import db, UsersTopics
from utils import need_authorization

__all__ = ['get_like', 'post_like', 'delete_like']


@need_authorization
@db
def get_like(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    query = UsersTopics.get_user_topic(**params).first()
    if not query is None:
        return {'liked': query.check_liked}

    return {'liked': 0}


@need_authorization
@db
def post_like(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    date = datetime.datetime.now()

    ut = UsersTopics.get_user_topic(**params).first()

    if ut is None:
        ut = UsersTopics(user_id=user.id, topic_name=name, liked=date)
        session.add(ut)
    else:
        ut.liked = date

    session.commit()


@need_authorization
@db
def delete_like(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    # Delete query
    ut = UsersTopics.get_user_topic(**params).first()
    if not ut is None:
        ut.liked = None
        session.commit()
