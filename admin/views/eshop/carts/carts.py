# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.carts.carts import Carts


class CartsModelView(SqlAlModelView):
    model = Carts
    category = u'Магазин'
    name = u'Корзины'

    column_list = ('users', 'items_cnt', 'status', 'cost_total', 'created', 'updated',)

    form_columns = ('users', 'status', 'created', 'updated',)

    column_labels = dict(
        users=u'Пользователь',
        items_cnt=u'Кол-во элементов',
        status=u'Статус',
        cost_total=u'Итоговая стоимость',
        created=u'Дата создания',
        updated=u'Дата обновления',
    )
