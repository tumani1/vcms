# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.persons_media import PersonsMedia


class PersonsMediaModelView(SqlAlModelView):
    model = PersonsMedia
    category = u'Медиа-объекты'
    name = u'Роль персоны'

    column_list = (
        'media', 'persons', 'role', 'type',
    )

    column_labels = dict(
        media=u'ID медиа',
        persons=u'ID персоны',
        role=u'Роль',
        type=u'Тип',
    )

    form_columns = (
        'media', 'persons', 'role', 'type',
    )

    column_filters = (
        'media.title', 'media.owner_id', 'persons.id', 'role',
    )

    form_ajax_refs = dict(
        persons={
            'fields': ('firstname', 'lastname',),
        },
        media={
            'fields': ('title',),
        },
    )

