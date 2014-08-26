# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.users_media_units import UsersMediaUnits


class UsersMediaUnitsModelView(SqlAlModelView):
    model = UsersMediaUnits
    category = u'Медиа-объекты'
    name = u'Отношение пользователей и медиа юнитов'

    column_list = ('media_units', 'users', 'subscribed', 'watched',)

    form_columns = ('media_units', 'users',)

    column_labels = dict(
        media_units=u'Идентификатор медиа юнита',
        users=u'Идентификатор пользователя',
        subscribed=u'Подписка',
        watched=u'Просмотрено',
    )

