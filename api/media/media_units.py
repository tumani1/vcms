# coding: utf-8

from api.serializers import mMediaUnitsSerializer
from models.media.media import Media


def get(auth_user, session, id,  **kwargs):
    data = {}
    instance = Media.get_units_by_media_id(auth_user, session, id).all()
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mMediaUnitsSerializer(**params).data
    return data
