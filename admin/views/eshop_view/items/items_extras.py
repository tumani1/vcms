# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.items.items_extras import ItemsExtras


class ItemsExtrasModelView(SqlAlModelView):
    model = ItemsExtras
    category = u'Магазин'
    name = u'Отношение элементов и доп.материалов'

    column_list = form_columns = ('items', 'extra', 'extras_type',)

    column_labels = dict(
        items=u'Элемент',
        extra=u'Доп. материал',
        extras_type=u'Тип доп материала',
    )

