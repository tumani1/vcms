# coding: utf-8
from models import MediaUnits
from api.media_unit.serializer import mMediaUnitsSerializer
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

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'text' in kwargs:
        params['text'] = str(kwargs['text']).strip()

    if 'batch' in kwargs:
        params['batch'] = str(kwargs['batch']).strip()

    if 'topic' in kwargs:
        params['topic'] = str(kwargs['topic']).strip()

    instance = MediaUnits.get_media_units_list(**params).all()
    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance,
        }
        data = mMediaUnitsSerializer(**serializer_params).data
    return data