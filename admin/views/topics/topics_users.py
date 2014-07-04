# coding: utf-8
from admin.views.base import SqlAlModelView
from models.topics import UsersTopics


class UsersTopicsModelView(SqlAlModelView):
    model = UsersTopics
    category = u'Пользователи'
    name = u'Топики пользователей'

    column_labels = dict(
        users=u'Пользователь',
        subscribed=u'Дата подписки',
        liked=u'Дата лайка',
        extra=u'Дополнительный материал',
        topics=u'Топик',
    )