# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.items.items import Items


class ItemsModelView(SqlAlModelView):
    model = Items
    category = u'Магазин'
    name = u'Элементы'

    column_list = form_columns = ('name', 'description', 'active', 'instock', 'added', 'price', 'price_old', 'is_digital',)

    column_labels = dict(
        name=u'Название',
        description=u'Описание',
        active=u'Активный',
        instock=u'В наличии',
        added=u'Добавлен',
        price=u'Цена',
        price_old=u'Старая цена',
        is_digital=u'цифровой',
    )
