from api.serializers.m_extra import mExtra
from models.eshop.categories import CategoriesExtras


def get(categories_id, auth_user, session=None, **kwargs):
    extras_list = []

    categories_extras = CategoriesExtras.join_with_extras(session, categories_id)

    for cat in categories_extras:
        extras_list.append(cat.extras)

    serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': extras_list,
    }

    data = mExtra(**serializer_params).data

    return data




