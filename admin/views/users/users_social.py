# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import fields

from models.users.constants import APP_USERSOCIAL_TYPE


class UsersSocialModelView(ModelView):
    form_overrides = dict(
        sType=fields.Select2Field
    )

    column_choices = dict(
        sType=APP_USERSOCIAL_TYPE,
    )

    column_labels = dict(user=u'Пользователь', sType=u'Социальная сеть',
                         sToken=u'Токен пользователя', created=u'Дата создания',
                         updated=u'Последнее обновление')

    form_choices = dict(
        sType=APP_USERSOCIAL_TYPE,
    )

    form_excluded_columns = ('updated', 'created', )
