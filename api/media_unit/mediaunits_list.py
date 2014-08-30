# coding: utf-8

from models.media import MediaUnits
from api.serializers import mMediaUnitsSerializer
from utils.validation import validate_list_int


def get(auth_user=None, session=None, **kwargs):
    data = {}
    params = {
        'user': auth_user,
        'session': session,
        'id': None,
        'text': None,
        'batch': None,
        'topic': None,
    }

    query = kwargs['query_params']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'text' in query:
        params['text'] = str(query['text']).strip()

    if 'batch' in query:
        params['batch'] = str(query['batch']).strip()

    if 'topic' in query:
        params['topic'] = str(query['topic']).strip()

    instance = MediaUnits.get_media_units_list(**params).all()
    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance,
        }
        data = mMediaUnitsSerializer(**serializer_params).data
    return data
