# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.variants.variants import Variants


class VariantsModelView(SqlAlModelView):
    model = Variants
    category = u'Магазин'
    name = u'Варианты'

    column_list = form_columns = ('items', 'name', 'description', 'active', 'stock_cnt', 'added', 'price', 'price_old', 'reserved_cnt',)

    column_labels = dict(
        items=u'Элемент',
        name=u'Название',
        description=u'Описание',
        active=u'Активный',
        stock_cnt=u'В наличии штук',
        added=u'Добавлен',
        price=u'Цена',
        price_old=u'Старая цена',
        reserved_cnt=u'Зарезервировано штук',
    )
