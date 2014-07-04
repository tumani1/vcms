# coding: utf-8
from admin.views.base import SqlAlModelView
from models.users import UsersExtras


class UsersExtrasModelView(SqlAlModelView):
    model = UsersExtras
    category = u'Пользователи'
    name = u'Дополнительные материалы'

    # form_overrides = dict(
    #     extra_type=fields.Select2Field
    # )
    #
    # column_choices = dict(
    #     extra_type=APP_USERSEXTRAS_TYPE,
    # )

    column_labels = dict(user=u'Пользователь', extra=u'Дополнительные материалы',)
    #
    # form_args = dict(
    #     extra_type=dict(
    #         label=u'Тип материалов',
    #         choices=APP_USERSEXTRAS_TYPE,
    #     ),
    #
    # )
