# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import fields

from models.users.constants import APP_USERSEXTRAS_TYPE


class UsersExtrasModelView(ModelView):
    form_overrides = dict(
        extra_type=fields.Select2Field
    )

    column_choices = dict(
        extra_type=APP_USERSEXTRAS_TYPE,
    )

    column_labels = dict(user=u'Пользователь', extra_type=u'Тип материалов',
                         extra=u'Дополнительные материалы',)

    form_args = dict(
        extra_type=dict(
            label=u'Тип материалов',
            choices=APP_USERSEXTRAS_TYPE,
        ),

    )
