# coding: utf-8

from api.media.media_list import get as get_media_list

__all__ = ['get_topic_media']


def get_topic_media(auth_user, name, **kwargs):
    return get_media_list(auth_user=auth_user, topic=name, **kwargs)
