# coding: utf-8
from api.media.serializer.m_media import mMediaSerializer
from models.media.media import Media
from utils.validation import validate_list_int

def get(auth_user=None, session=None, **kwargs):
    params = {
        'user': auth_user,
        'session': session,
        'id': None,
        'text': None,
        'topic': None,
    }

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'topic' in kwargs:
        params['topic'] = str(kwargs['topic']).strip()

    if 'text' in kwargs:
        params['text'] = str(kwargs['text']).strip()

    if 'units' in kwargs:
        params['units'] = validate_list_int(kwargs['units'])

    if 'releasedate' in kwargs:
        params['releasedate'] = str(kwargs['releasedate']).strip()

    if 'persons' in kwargs:
        params['persons'] = validate_list_int(kwargs['persons'])

    instance = Media.get_media_list(**params).all()
    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance,
        }
        data = mMediaSerializer(**serializer_params).data
    return data