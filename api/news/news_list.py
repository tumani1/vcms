# coding: utf-8
from api.serializers import mNewsSerializer

from models import News
from utils.validation import validate_mLimit


def get(auth_user, session=None, **kwargs):

    data = {}

    params = {
        'session': session,
        'id': None,
        'limit': None,
        'sort': None,
        'with_obj': None,
        'obj_type': None,
        'obj_id': None,
        'obj_name': None
    }

    query = kwargs['query_params']

    if 'id' in query:
        params['id'] = query['id']

    if 'limit' in query:
        params['limit'] = validate_mLimit(query['limit'])

    if 'sort' in query:
        params['sort'] = query['sort']

    if 'with_obj' in query:
        with_obj = query['with_obj'].lower()

        if with_obj == 'false':
            params['with_obj'] = False
        else:
            params['with_obj'] = True
    else:
        params['with_obj'] = False

    if 'obj_type' in query:
        params['obj_type'] = query['obj_type']

    if 'obj_id' in query:
        params['obj_id'] = query['obj_id']

    if 'obj_name' in query:
        params['obj_name'] = query['obj_name']

    news_list = News.get_news_list(**params).all()

    if not news_list is None:
        serializer_params = {
            'with_obj': params['with_obj'],
            'instance': news_list,
            'user': auth_user,
            'session': session,
        }
        data = mNewsSerializer(**serializer_params).data

    return data


