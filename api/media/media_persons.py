# coding: utf-8

from utils.validation import validate_list_int, validate_mLimit
from models.media.media import Media
from api.serializers import mPersonRoleSerializer


def get(auth_user, session, **kwargs):
    params = {
        'id': None,
        'is_online': None,
        'limit': None,
        'session': session,
    }

    query = kwargs['query']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'is_online' in query and query['is_online']:
        params['is_online'] = query['is_online']

    if 'limit' in query:
        params['limit'] = validate_mLimit(query['limit'])

    instance = Media.get_persons_by_media_id(auth_user, **params)

    new_param = {
        'instance': instance,
        'user': auth_user,
        'session': session,
    }
    return mPersonRoleSerializer(**new_param).data
