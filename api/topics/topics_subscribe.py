# coding: utf-8

import datetime

from utils import need_authorization
from models import db, UsersTopics

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@need_authorization
@db
def get_subscribe(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    query = UsersTopics.get_user_topic(**params).first()

    if not query is None:
        return query.check_subscribed

    return False


@need_authorization
@db
def post_subscribe(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    date = datetime.datetime.now()
    ut = UsersTopics.get_user_topic(**params).first()

    if ut is None:
        ut = UsersTopics(user_id=user.id, topic_name=name, subscribed=date)
        session.add(ut)
    else:
        ut.subscribed = date

    session.commit()


@need_authorization
@db
def delete_subscribe(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    # Delete query
    ut = UsersTopics.get_user_topic(**params).first()
    if not ut is None:
        ut.subscribed = None
        session.commit()
