from models import db, MediaUnits
from api.media_unit.serializer import mMediaUnitsSerializer


@db
def get(user=None, session=None, **kwargs):
    params = {
        'user': user,
        'session': session,
        'id': None,
        'text': None,
        'batch': None,
        'topic': None,
    }

    if 'id' in kwargs:
        params['id'] = str(kwargs['id']).strip()

    if 'text' in kwargs:
        params['text'] = str(kwargs['text']).strip()

    if 'batch' in kwargs:
        params['batch'] = str(kwargs['batch']).strip()

    if 'topic' in kwargs:
        params['topic'] = str(kwargs['topic']).strip()

    instance = MediaUnits.get_media_units_list(**params)
    serializer_params = {
        'user': user,
        'session': session,
        'instance': instance,
    }
    return mMediaUnitsSerializer(**serializer_params).data