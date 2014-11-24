# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.carts.items_carts import ItemsCarts


class ItemsCartsModelView(SqlAlModelView):
    model = ItemsCarts
    category = u'Магазин'
    name = u'Отношение элементов и корзин'

    column_list = form_columns = ('carts', 'variants', 'cnt', 'price', 'cost', 'added',)

    column_labels = dict(
        carts=u'Корзина',
        variants=u'Вариант элемента',
        cnt=u'Кол-во',
        price=u'Цена',
        cost=u'Стоимость',
        added=u'Дата добавления',
    )


