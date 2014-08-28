from api.serializers.m_shop_cart_item import mShopCartItem
from models import Carts, ItemsCarts
from utils import need_authorization


@need_authorization
def get(auth_user, session=None, **kwargs):
    cart = Carts.get_cart_active_by_user_id(session, auth_user.id).first()

    items_carts = ItemsCarts.get_items_carts_by_carts_id(session, cart.id).all()

    serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': items_carts,
    }

    data = mShopCartItem(**serializer_params).data

    return data



