# coding: utf-8
from wtforms.fields import StringField

from admin.views.base import BaseModelView
from models.cdn import CDN


class CdnModelView(BaseModelView):
    model = CDN

    category = u'CDN'
    name = u'CDN'

    column_labels = dict(name=u'Название', description=u'Описание',
                         cdn_type=u'Тип', url=u'URL адресс',
                         has_mobile=u'Для мобильных устройств',
                         has_auth=u'Необходима авторизация',
                         location_regxp=u'Регулярное вырожожение для локации',
                         )

    column_list = ('name', 'has_mobile', 'has_auth', 'description', 'cdn_type',
                   'url', 'location_regxp')

    form_excluded_columns = ('extras', 'media_locations', )
    form_overrides = dict(
        name=StringField,
    )

    form_columns = column_list

    form_args = dict(
        name=dict(
            label=u'Название',
        ),
    )