# coding: utf-8
from admin.views.base import BaseModelView
from models.persons import UsersPersons


class PersonsUsersModelView(BaseModelView):
    model = UsersPersons
    category = u'Персоны'
    name = u'Персоны пользователя'

    column_labels = dict(
        users=u'Пользователь',
        subscribed=u'Дата подписки',
        liked=u'Дата лайка',
    )
