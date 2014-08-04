# coding: utf-8

import datetime

from utils import need_authorization
from models.topics import UsersTopics

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@need_authorization
def get_subscribe(name, auth_user, session, **kwargs):
    params = {
        'user': auth_user,
        'name': name,
        'session': session,
    }

    query = UsersTopics.get_user_topic(**params).first()

    if not query is None:
        return {'subscribed': query.check_subscribed}

    return {'subscribed': False}


@need_authorization
def post_subscribe(name, auth_user, session, **kwargs):
    params = {
        'user': auth_user,
        'name': name,
        'session': session,
    }

    date = datetime.datetime.utcnow()
    ut = UsersTopics.get_user_topic(**params).first()

    if ut is None:
        ut = UsersTopics(user_id=auth_user.id, topic_name=name, subscribed=date)
        session.add(ut)
    else:
        ut.subscribed = date

    session.commit()


@need_authorization
def delete_subscribe(name, auth_user, session, **kwargs):
    params = {
        'user': auth_user,
        'name': name,
        'session': session,
    }

    # Delete query
    ut = UsersTopics.get_user_topic(**params).first()
    if not ut is None:
        ut.subscribed = None
        session.commit()
