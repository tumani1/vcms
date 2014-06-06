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
    ut = UsersTopics(user_id=user.id, topic_name=name, subscribed=datetime.datetime.now())
    session.add(ut)
    session.commit()
    # try:
    #     session.commit()
    # except Exception, e:
    #     return {'error': e.message, 'code': 400}


@need_authorization
@db
def delete_subscribe(user, name, session, **kwargs):
    params = {
        'user': user.id,
        'name': name,
        'session': session,
    }

    # Delete query
    UsersTopics.get_user_topic(**params).delete()
