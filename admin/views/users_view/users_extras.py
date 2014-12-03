# coding: utf-8
from admin.views.base import SqlAlModelView
from models.users import UsersExtras


class UsersExtrasModelView(SqlAlModelView):
    model = UsersExtras
    category = u'Пользователи'
    name = u'Дополнительные материалы'

    column_labels = dict(user=u'Пользователь', extra=u'Дополнительные материалы',)
