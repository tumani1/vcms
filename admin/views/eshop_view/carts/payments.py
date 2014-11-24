# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.carts.payments import Payments


class PaymentsModelView(SqlAlModelView):
    model = Payments
    category = u'Магазин'
    name = u'Платежи'

    column_list = ('carts', 'status', 'created', 'payed', 'pay_system', 'cost',)
    form_columns = ('carts', 'status', 'created',)

    column_labels = dict(
        carts=u'Корзина',
        status=u'Статус',
        created=u'Дата создания',
        payed=u'Дата оплаты',
        pay_system=u'Платежная система',
        cost=u'Стоимость',
    )


