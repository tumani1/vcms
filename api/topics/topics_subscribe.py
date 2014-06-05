# coding: utf-8

import datetime
from models import db, UsersTopics

__all__ = ['get_subscribe', 'post_subscribe', 'delete_subscribe']


@db
def get_subscribe(user, name, session, **kwargs):
    if not user is None:
        params = {
            'user': user.id,
            'name': name,
            'session': session,
        }

        query = UsersTopics.get_user_topic(**params).first()

        if not query is None:
            return query.check_subscribed

        return False

    return {'error': 403}


@db
def post_subscribe(user, session, name, **kwargs):
    if not user is None:
        ut = UsersTopics(user_id=user.id, topic_name=name, subscribed=datetime.datetime.now())
        session.add(ut)
        session.commit()

    return {'error': 403}


@db
def delete_subscribe(user, session, name, **kwargs):
    if not user is None:
        pass

    return {'error': 403}
