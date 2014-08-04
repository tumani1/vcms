# coding: utf-8
from api.serializers.m_media import mMediaSerializer
from models.media.media import Media


def get(id, auth_user, session, **kwargs):
    data = {}
    instance = Media.get_media_by_id(auth_user, session, id)
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mMediaSerializer(**params).data
    return data

