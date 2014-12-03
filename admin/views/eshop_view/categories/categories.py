# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.categories.categories import Categories


class CategoriesModelView(SqlAlModelView):
    model = Categories
    category = u'Магазин'
    name = u'Категории'

    column_list = form_columns = ('name', 'description', )

    column_labels = dict(
        name=u'Название',
        description=u'Описание',
    )

