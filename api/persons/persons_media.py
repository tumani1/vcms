# coding: utf-8

from api.media.media_list import get as get_media_list

__all__ = ['get_person_media']


def get_person_media(person_id, auth_user, session, **kwargs):
    params = {'query': {'persons': person_id}}
    return get_media_list(auth_user=auth_user, session=session, **params)
