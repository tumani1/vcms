# coding: utf-8

from admin.views.base import SqlAlModelView
from models.eshop.items.users_items import UsersItems


class UsersItemsModelView(SqlAlModelView):
    model = UsersItems
    category = u'Магазин'
    name = u'Отношение элементов и пользователей'

    column_list = ('items', 'users', 'watched', 'bought_cnt', 'wished', 'dontlike',)
    form_columns = ('items', 'users', )

    column_labels = dict(
        items=u'Элемент',
        users=u'Пользователь',
        watched=u'Дата просмотра',
        bought_cnt=u'Куплено штук',
        wished=u'Дата установки признака "Хочу"',
        dontlike=u'Дата дизлайка',
    )


