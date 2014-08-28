from models import Carts, ItemsCarts
from utils import need_authorization


@need_authorization
def get(auth_user, session=None, **kwargs):
    data = {
        'items_cnt': '',
        'total_cnt': '',
        'cost': '',
        'id': ''
    }

    cart = Carts.get_cart_active_by_user_id(session, auth_user.id).first()

    data['items_cnt'] = cart.items_cnt
    data['cost'] = cart.cost_total
    data['id'] = cart.id

    items_carts = ItemsCarts.get_items_carts_by_carts_id(session, cart.id).all()

    data['total_cnt'] = items_carts.__len__()

    return data



