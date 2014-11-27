# coding: utf-8
from admin.views.base import SqlAlModelView
from models.comments.users_comments import UsersComments


class UsersCommentsModelView(SqlAlModelView):
    model = UsersComments
    category = u'Комментарии'
    name = u'Отношение пользователей и комментариев'

    column_list = ('users', 'comments', 'liked',)

    column_labels = dict(
        users=u'ID пользователя',
        comments=u'ID комментария',
        liked=u'Дата лайка',
    )

    form_columns = ('users', 'comments',)


