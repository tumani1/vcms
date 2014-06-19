# coding: utf-8

import datetime

from utils import need_authorization
from models import UsersTopics
from db_engine import db

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@need_authorization
@db
def get_subscribe(auth_user, name, session, **kwargs):
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
@db
def post_subscribe(auth_user, name, session, **kwargs):
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
@db
def delete_subscribe(auth_user, name, session, **kwargs):
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
