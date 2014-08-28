from api.serializers.m_extra import mExtra
from models import Categories, ItemsCategories, CategoriesExtras


def get(categories_id, auth_user, session=None, **kwargs):
    extras_list = []
    data = {
        'items_cnt': '',
        'instock_cnt': '',
        'name': '',
        'description': '',
        'extras': ''
    }
    categories = Categories.get_categories_by_id(session, categories_id).first()

    data['name'] = categories.name
    data['description'] = categories.description

    items_categories = ItemsCategories.get_items_categories_by_category_id(session, categories_id).all()

    data['items_cnt'] = items_categories.__len__()

    items = ItemsCategories.get_item_by_category_id(session, categories_id).all()

    data['instock_cnt'] = items.__len__()

    categories_extras = CategoriesExtras.join_with_extras(session, categories_id).all()

    for cat in categories_extras:
        extras_list.append(cat.extras)

    serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': extras_list,
    }

    data['extras'] = mExtra(**serializer_params).data

    return data






