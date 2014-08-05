# coding: utf-8
from api.serializers.m_media import mMediaSerializer
from models.media.media import Media
from utils.validation import validate_int


def get(id, auth_user, session, **kwargs):
    data = {}
    id = validate_int(id, min_value=1)
    instance = Media.get_media_by_id(auth_user, session, id)
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mMediaSerializer(**params).data
    return data

