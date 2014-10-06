from api.serializers.m_shop_cart import mShopCart
from models import Carts
from utils import need_authorization
from utils.validation import validate_mLimit


@need_authorization
def get(auth_user, session, **kwargs):
    items = []
    data = {
        'cnt': '',
        'total_cnt': '',
        'items': ''
    }

    params = {
        'session': session,
        'user_id': auth_user.id,
        'limit': None,
        'top': None
    }

    query = kwargs['query_params']

    if 'limit' in query:
        limit, top = validate_mLimit(query['limit'])
        params['limit'] = limit
        params['top'] = top

    carts = Carts.get_cart_by_user_id(session, auth_user.id).all()

    data['total_cnt'] = carts.__len__()

    carts_limit = Carts.get_cart_limit_by_user_id(**params).all()

    data['cnt'] = carts_limit.__len__()

    for cart in carts_limit:
        serializer_params = {
                'user': auth_user,
                'session': session,
                'instance': Carts.tmpl_for_carts(cart.id, session).first(),
        }
        items.append(mShopCart(**serializer_params).data)

    data['items'] = items

    return data






