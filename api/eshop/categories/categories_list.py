from models import Categories


def get(auth_user, session=None, **kwargs):
    data = []
    categories = {
        'id': '',
        'name': ''
    }
    params = {
        'session': session,
        'instock': None,
        'has_items': None,
        'sort': None
    }

    query = kwargs['query']

    if 'instock' in query:
        params['instock'] = query['instock']

    if 'has_items' in query:
        params['has_items'] = query['has_items']

    if 'sort' in query:
        params['sort'] = query['sort']

    Categories.get_list_categories(**params)


