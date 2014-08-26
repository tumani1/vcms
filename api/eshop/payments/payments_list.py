from models import Payments, Carts
from utils import need_authorization
from utils.validation import validate_mLimit


@need_authorization
def get(**kwargs):
    auth_user = kwargs['auth_user']
    session = kwargs['session']
    limit = kwargs.get('limit', '')
    limit, top = validate_mLimit(limit)
    carts = session.query(Carts).filter_by(user_id=auth_user.id)
    payments = session.query(Payments).filter(Payments.cart_id.in_([c.id for c in carts]))
    if top:
        payments = payments.offset(top)
    if limit:
        payments = payments.limit(limit)

    return payments
