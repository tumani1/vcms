# coding: utf-8

from api.serializers import mCommentSerializer
from models.comments.comments import Comments
from utils.validation import validate_list_int, validate_mLimitId, validate_string, validate_obj_type


def get(auth_user=None, session=None, **kwargs):
    params = {
        'user': auth_user,
        'session': session,
        'id': None,
        'obj_type': None,
        'obj_id': None,
        'obj_name': None,
        'user_id': None,
        'with_obj': None,
        'limit': validate_mLimitId('10'),
    }

    query = kwargs['query_params']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'user_id' in query:
        params['user_id'] = validate_list_int(query['user_id'])

    if 'obj_id' in query:
        params['obj_id'] = validate_list_int(query['obj_id'])

    if 'obj_name' in query:
        params['obj_name'] = validate_string(query['obj_name'])

    if 'limit' in query:
        params['limit'] = validate_mLimitId(query['limit'])

    if 'obj_type' in query:
        params['obj_type'] = validate_obj_type(query['obj_type'])

    if 'with_obj' in query:
        params['with_obj'] = query['with_obj']

    instance = Comments.get_comments_list(**params)
    instance = Comments.mLimitId(instance, params['limit'])
    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance.all(),
            'with_obj': params['with_obj']
        }
        data = mCommentSerializer(**serializer_params).data
    return data
