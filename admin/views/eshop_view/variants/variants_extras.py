# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.variants.variants_extras import VariantsExtras


class VariantsExtrasModelView(SqlAlModelView):
    model = VariantsExtras
    category = u'Магазин'
    name = u'Отношение вариантов и доп.материалов'

    column_list = form_columns = ('variants', 'extra', 'extras_type',)

    column_labels = dict(
        variants=u'Вариант',
        extra=u'Доп. материал',
        extras_type=u'Тип доп материала',
    )
