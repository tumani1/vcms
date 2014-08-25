# coding: utf-8
from wtforms.fields import StringField

from admin.views.base import SqlAlModelView
from models.cdn import CDN


class CdnModelView(SqlAlModelView):
    model = CDN

    category = u'CDN'
    name = u'CDN'

    column_labels = dict(name=u'Название', description=u'Описание',
                         cdn_type=u'Тип', url=u'URL адресс',
                         has_mobile=u'Для мобильных устройств',
                         has_auth=u'Необходима авторизация',
                         location_regxp=u'Регулярное вырожожение для локации', )

    form_columns = column_list = ('name', 'has_mobile', 'has_auth', 'cdn_type',
                                  'url', 'location_regxp', 'description', )

    form_excluded_columns = ('extras', 'media_locations', )
    form_overrides = dict(
        name=StringField,
    )
