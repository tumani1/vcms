# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.media_in_unit import MediaInUnit


class MediaInUnitModelView(SqlAlModelView):
    model = MediaInUnit
    category = u'Медиа-объекты'
    name = u'Отношение медиа и юнитов'

    form_columns = column_list = ('media', 'media_units', 'm_order', )

    column_labels = dict(
        media=u'Идентификатор медиа',
        media_units=u'Идентификатор юнита',
        m_order=u'Порядок',
    )
