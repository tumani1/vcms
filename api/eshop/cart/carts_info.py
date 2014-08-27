from api.serializers.m_shop_cart import mShopCart
from models import Carts
from utils import need_authorization


@need_authorization
def get(carts_id, auth_user, session, **kwargs):
    carts = Carts.tmpl_for_carts(carts_id, session).first()

    serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': carts,
    }

    data = mShopCart(**serializer_params).data

    return data

