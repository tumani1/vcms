# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.users_media import UsersMedia


class UsersMediaModelView(SqlAlModelView):
    model = UsersMedia
    category = u'Медиа-объекты'
    name = u'Отношение пользователей и медиа'

    column_list = ('media', 'users', 'views_cnt', 'liked', 'playlist', 'play_pos', 'watched',)

    form_columns = ('media', 'users',)

    column_labels = dict(
        media=u'Идентификатор медиа',
        users=u'Идентификатор пользователя',
        views_cnt=u'Кол-во просмотров',
        liked=u'Лайк',
        playlist=u'В плейлисте',
        play_pos=u'Позиция проигрывания',
        watched=u'Просмотрено',
    )

