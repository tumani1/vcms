# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.variants.variants_scheme import VariantsScheme


class VariantsSchemeModelView(SqlAlModelView):
    model = VariantsScheme
    category = u'Магазин'
    name = u'Схемы вариантов'

    column_list = form_columns = ('categories', 'name', 'description', 'type', 'default', 'enable')

    column_labels = dict(
        categories=u'Категория',
        name=u'Название',
        description=u'Описание',
        type=u'Тип',
        default=u'По умолчанию',
        enable=u'Разрешение',
    )

