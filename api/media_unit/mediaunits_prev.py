# coding: utf-8

from models.media import MediaUnits
from api.media_unit.serializer import mMediaUnitsSerializer


def get(id, auth_user, session, **kwargs):
    instance = MediaUnits.get_prev_media_unit(auth_user, session, id)
    data = {}
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mMediaUnitsSerializer(**params).data
    return data
