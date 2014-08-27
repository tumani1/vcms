from api.serializers.m_shop_cart_item import mShopCartItem
from models import ItemsCarts
from utils import need_authorization


@need_authorization
def get(carts_id, auth_user, session, **kwargs):
    items_carts = ItemsCarts.get_items_carts_by_carts_id(session, carts_id).all()

    serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': items_carts,
    }

    data = mShopCartItem(**serializer_params).data

    return data

