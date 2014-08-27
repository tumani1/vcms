from api.serializers.m_shop_cart_log import mShopCartLog
from models import CartLog
from utils import need_authorization


@need_authorization
def get(carts_id, auth_user, session, **kwargs):
    carts = CartLog.get_cart_log_by_cart_id(session, carts_id).all()

    serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': carts,
    }

    data = mShopCartLog(**serializer_params).data

    return data
