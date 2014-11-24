# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.persons_media import PersonsMedia


class PersonsMediaModelView(SqlAlModelView):
    model = PersonsMedia
    category = u'Медиа-объекты'
    name = u'Отношение персон и медиа'

    column_list = form_columns = ('media', 'persons', 'role', 'type', )

    column_labels = dict(
        media=u'Идентификатор медиа',
        persons=u'Идентификатор персоны',
        role=u'Роль',
        type=u'Тип',
    )

