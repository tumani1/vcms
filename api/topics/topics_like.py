# coding: utf-8

from models import dbWrap, UsersTopics

__all__ = ['get_like', 'post_like', 'delete_like']


@dbWrap
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


@dbWrap
def post_like(user, session, name, **kwargs):
    if not user is None:
        pass

    return {'error': 403}


@dbWrap
def delete_like(user, session, name, **kwargs):
    if not user is None:
        pass

    return {'error': 403}
