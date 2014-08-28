# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.categories.categories_extras import CategoriesExtras


class CategoriesExtrasModelView(SqlAlModelView):
    model = CategoriesExtras
    category = u'Магазин'
    name = u'Отношение категорий и доп.материалов'

    column_list = form_columns = ('categories', 'extra', 'extras_type',)

    column_labels = dict(
        categories=u'Категория',
        extra=u'Доп. материал',
        extras_type=u'Тип доп материала',
    )

