from api.eshop.items.items_list import get as get_list

def get(categories_id, auth_user, session=None, **kwargs):
    params = {'query_params': {'cat': categories_id}}
    return get_list(auth_user, session, **params)
