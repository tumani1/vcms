# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.carts.cart_log import CartLog


class CartLogModelView(SqlAlModelView):
    model = CartLog
    category = u'Магазин'
    name = u'Лог корзины'

    column_list = form_columns = ('carts', 'status', 'time', 'comment',)

    column_labels = dict(
        carts=u'Корзина',
        status=u'Статус',
        time=u'Время',
        comment=u'Комментарий',
    )

