# coding: utf-8
from admin.views.base import SqlAlModelView
from models.comments.users_comments import UsersComments


class UsersCommentsModelView(SqlAlModelView):
    model = UsersComments
    category = u'Комментарии'
    name = u'Отношение пользователей и комментариев'

    column_list = ('users', 'comments', 'liked',)

    form_columns = ('users', 'comments',)

    column_labels = dict(
        users=u'Идентификатор пользователя',
        comments=u'Идентификатор комментария',
        liked=u'Дата лайка',
    )


