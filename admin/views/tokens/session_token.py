# coding: utf-8
from admin.views.base import BaseModelView
from models.tokens import SessionToken


class SessionTokenModelView(BaseModelView):
    model = SessionToken
    category = u'Токены пользователя'
    name = u'Токен сэссии'

    column_list = ('token', 'user', 'is_active', 'created')

    column_labels = dict(token=u'Токен', user=u'Пользователь',
                         created=u'Дата создания', is_active=u'Активность')

    form_columns = ('user', 'is_active', )