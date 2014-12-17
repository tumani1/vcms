# coding: utf-8

from models import Users, Media

__all__ = ['get_stat_list']


def get_stat_list(auth_user, session, **kwargs):
    result = kwargs['mc'].get('service_stat')

    if result is None:
        media_cnt, views_cnt = Media.media_cnt(session)

        result = {
            'users_cnt': Users.users_cnt(session)[0],
            'media_cnt': media_cnt,
            'views_cnt': views_cnt,
        }

        kwargs['mc'].set('service_stat', result, 1800)

    return result
