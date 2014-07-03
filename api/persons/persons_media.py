# coding: utf-8

from api.media.media_list import get as get_media_list

__all__ = ['get_person_media']


def get_person_media(auth_user, id, session, **kwargs):
    return get_media_list(auth_user=auth_user, persons=id, session=session, **kwargs)
