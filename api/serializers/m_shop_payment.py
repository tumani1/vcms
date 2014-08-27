from utils.common import datetime_to_unixtime


class mShopPayment(object):

    def __init__(self, payment):
        self.p = payment

    def get_data(self):
        return {'id': self.p.id,
                'cart_id': self.p.cart_id,
                'created': datetime_to_unixtime(self.p.created),
                'status': self.p.status,
                'cost': self.p.cost,
                'payed': datetime_to_unixtime(self.p.payed),
                'pay_system': self.p.pay_system}