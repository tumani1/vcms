# coding: utf-8
from models.media.media_units import MediaUnits
from serializer import mMediaUnitsSerializer


def get(auth_user, session, id, **kwargs):
    data = {}
    instance = MediaUnits.get_media_unit_by_id(auth_user, session, id)
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mMediaUnitsSerializer(**params).data
    return data