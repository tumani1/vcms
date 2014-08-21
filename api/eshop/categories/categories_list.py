import copy
from models import Categories


def get(session=None, **kwargs):
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

    category = Categories.get_list_categories(**params)

    for cat in category:
        categories['id'] = cat.id
        categories['name'] = cat.name
        data.append(copy.deepcopy(categories))

    return data




