# coding: utf-8
from api.serializers.m_media import mMediaSerializer
from models.media.media import Media
from utils.validation import validate_list_int


def get(auth_user=None, session=None, **kwargs):
    data = {}
    params = {
        'user': auth_user,
        'session': session,
        'id': None,
        'text': None,
        'units': None,
        'releasedate': None,
        'persons': None,
    }

    query = kwargs['query']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'topic' in query:
        params['topic'] = str(query['topic']).strip()

    if 'text' in query:
        params['text'] = str(query['text']).strip()

    if 'units' in query:
        params['units'] = validate_list_int(query['units'])

    if 'releasedate' in query:
        params['releasedate'] = validate_list_int(query['releasedate'])

    if 'persons' in query:
        params['persons'] = validate_list_int(query['persons'])

    instance = Media.get_media_list(**params).all()
    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance,
        }
        data = mMediaSerializer(**serializer_params).data

    return data
