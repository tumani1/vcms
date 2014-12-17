# coding: utf-8

from admin.fields import SelectField
from admin.views.base import SqlAlModelView
from models.media.constants import APP_MEDIA_TYPE_WITH_DEFAULT, APP_MEDIA_LIST
from models.media.media_access_defaults import MediaAccessDefaults


class MediaAccessDefaultsModelView(SqlAlModelView):
    model = MediaAccessDefaults
    category = u'Медиа-объекты'
    name = u'Доступ к медиа с типом default'

    column_list = form_columns = ('name', 'access', 'access_type',)

    column_labels = dict(
        name=u'Тип медиа',
        access=u'Доступ',
        access_type=u'Тип доступа',
    )

    form_overrides = dict(
        name=SelectField,
        access_type=SelectField,
    )

    column_choices = dict(
        name=APP_MEDIA_TYPE_WITH_DEFAULT,
        access_type=APP_MEDIA_LIST,
    )

    form_choices = dict(
        name=APP_MEDIA_TYPE_WITH_DEFAULT,
        access_type=APP_MEDIA_LIST,
    )

    form_args = dict(
        name=dict(
            choices=APP_MEDIA_TYPE_WITH_DEFAULT,
        ),
        access_type=dict(
            choices=APP_MEDIA_LIST,
        ),
    )