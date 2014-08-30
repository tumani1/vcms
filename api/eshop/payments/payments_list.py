from models import Payments, Carts
from utils import need_authorization
from utils.validation import validate_mLimit
from api.serializers import mShopPayment as mSP


@need_authorization
def get(**kwargs):
    auth_user = kwargs['auth_user']
    session = kwargs['session']
    limit = kwargs['query_params'].get('limit', '')
    limit, top = validate_mLimit(limit)
    carts = session.query(Carts).filter_by(user_id=auth_user.id)
    payments = session.query(Payments).filter(Payments.cart_id.in_([c.id for c in carts]))
    total_count = payments.count()
    if top:
        payments = payments.offset(top)
    if limit:
        payments = payments.limit(limit)
    current_count = payments.count()
    items = [mSP(p).get_data() for p in payments]

    return {'cnt': current_count, 'total_cnt': total_count, 'items': items}
