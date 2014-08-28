# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.variants.variants_values import VariantsValues


class VariantsValuesModelView(SqlAlModelView):
    model = VariantsValues
    category = u'Магазин'
    name = u'Отношение вариантов и значений'

    column_list = form_columns = ('variants_scheme', 'variants', 'name', 'value',)

    column_labels = dict(
        variants=u'Вариант',
        variants_scheme=u'Схема',
        name=u'Название',
        value=u'Значение',
    )

