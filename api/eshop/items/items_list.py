# coding: utf-8
from utils.validation import validate_list_int, validate_mLimit, validate_eshop_price, validate_eshop_sort
from models.eshop.items.items import Items
from api.serializers.m_shop_item import mShopItem


def get(auth_user, session, **kwargs):
    data = {}
    params = {
        'user': auth_user,
        'session': session,
        'limit': validate_mLimit(limit='10'),
        'id': None,
        'instock': None,
        'name': None,
        'text': None,
        'price': None,
        'is_watched': None,
        'is_bought': None,
        'sort': None,
        'sort_desc': None,
        'cat': None,
        'values': None,
        'obj_type': None,
        'obj_id': None,
        'obj_name': None,
        'is_digital': None,
    }

    query = kwargs['query']

    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'limit' in query:
        params['limit'] = validate_mLimit(limit=query['limit'])

    if 'name' in query:
        params['name'] = str(query['name']).strip()

    if 'text' in query:
        params['text'] = str(query['text']).strip()

    if 'instock' in query:
        params['instock'] = query['instock']

    if 'price' in query:
        params['price'] = validate_eshop_price(query['price'])

    if 'is_watched' in query:
        params['is_watched'] = query['is_watched']

    if 'is_bought' in query:
        params['is_bought'] = query['is_bought']

    if 'sort' in query:
        params['sort'] = validate_eshop_sort(query['sort'])
        if 'sort_desc' in query:
            params['sort_desc'] = query['sort_desc']

    if 'cat' in query:
        params['cat'] = validate_list_int(query['cat'])

    if 'values' in query:
        params['values'] = query['values']

    if 'obj_type' in query:
        params['obj_type'] = query['obj_type']

    if 'obj_id' in query:
        params['obj_id'] = query['obj_id']

    if 'obj_name' in query:
        params['obj_name'] = query['obj_name']

    if 'is_digital' in query:
        params['is_digital'] = query['is_digital']

    instance = Items.get_items_list(**params)

    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance.all(),
        }
        data = mShopItem(**serializer_params).data
    return data