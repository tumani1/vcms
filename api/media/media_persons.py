from utils.validation import validate_list_int, validate_mLimit
from models.media.media import Media
from api.persons.serializer import mPersonRoleSerializer


def get(auth_user, session, **kwargs):
    params = {
        'id': None,
        'is_online': None,
        'limit': None,
        'session': session,
    }

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'is_online' in kwargs and kwargs['is_online']:
        params['is_online'] = kwargs['is_online']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(kwargs['limit'])

    instance = Media.get_persons_by_media_id(auth_user, **params)

    new_param = {
        'instance': instance,
        'user': auth_user,
        'session': session,
    }
    return mPersonRoleSerializer(**new_param).data