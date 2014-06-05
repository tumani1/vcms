# coding: utf-8

from models import db, UsersTopics

__all__ = ['get_like', 'post_like', 'delete_like']


@db
def get_like(user, session, name, **kwargs):
    if not user is None:
        params = {
            'user': user.id,
            'name': name,
            'session': session,
        }

        query = UsersTopics.get_user_topic(**params).first()

        if not query is None:
            return query.check_liked

        return False

    return {'error': 403}


@db
def post_like(user, session, name, **kwargs):
    if not user is None:
        pass

    return {'error': 403}


@db
def delete_like(user, session, name, **kwargs):
    if not user is None:
        pass

    return {'error': 403}
