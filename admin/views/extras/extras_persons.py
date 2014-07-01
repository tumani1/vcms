# coding: utf-8
from admin.views.base import BaseModelView
from models.extras import PersonsExtras


class PersonsExtrasModelView(BaseModelView):
    model = PersonsExtras
    category = u'Персоны'
    name = u'Дополнительные материлы'

    column_display_pk = True

    column_labels = dict(
        extra_type=u'Тип доп. материала',
        extra=u'Дополнительный материал',
        persons=u'Персона',
    )