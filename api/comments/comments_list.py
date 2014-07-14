# coding: utf-8
from api.comments.serializer.m_comment import mCommentSerializer
from models.comments.comments import Comments
from utils.validation import validate_list_int, validate_int, validate_mLimitId, validate_string, validate_obj_type


def get(auth_user=None, session=None, **kwargs):
    params = {
        'user': auth_user,
        'session': session,
        'id': None,
        'obj_type': None,
        'obj_id': None,
        'obj_name': None,
        'user_id': None,
        'limit': None,
    }

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'user_id' in kwargs:
        params['user_id'] = validate_list_int(kwargs['user_id'])

    if 'obj_id' in kwargs:
        params['obj_id'] = validate_list_int(kwargs['obj_id'])

    if 'obj_name' in kwargs:
        params['obj_name'] = validate_string(kwargs['obj_name'])

    if 'limit' in kwargs:
        params['limit'] = validate_mLimitId(kwargs['limit'])

    if 'obj_type' in kwargs:
        params['obj_type'] = validate_obj_type(kwargs['obj_typy'])

    instance = Comments.get_comments_list(**params).all()
    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance,
        }
        data = mCommentSerializer(**serializer_params).data
    return data