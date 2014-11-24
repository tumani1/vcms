# coding: utf-8
from flask.ext.admin.form import fields
from admin.views.base import SqlAlModelView
from models.media.constants import APP_MEDIA_TYPE, APP_MEDIA_LIST
from models.media.media import Media


class MediaModelView(SqlAlModelView):
    model = Media
    category = u'Медиа-объекты'
    name = u'Медиа'

    column_list = ('title', 'title_orig', 'allow_mobile', 'allow_smarttv', 'allow_external', 'allow_anon', 'description', 'created',
                    'views_cnt', 'release_date', 'poster', 'duration', 'user_owner', 'type_', 'access', 'access_type' )

    form_columns = ('title', 'title_orig', 'allow_mobile', 'allow_smarttv', 'allow_external', 'allow_anon', 'description'
                    , 'release_date', 'poster', 'duration', 'user_owner', 'type_', 'access', 'access_type' )

    column_labels = dict(
        title=u'Заголовок',
        title_orig=u'Оригинальное название',
        allow_mobile=u'Доступны на моб.телефонах',
        allow_smarttv=u'Доступны на Smart TV',
        allow_external=u'Доступны внешние ссылки',
        allow_anon=u'Доступна анонимность',
        description=u'Описание',
        views_cnt=u'Количество просмотров',
        release_date=u'Дата выхода',
        poster=u'Постер',
        duration=u'Продолжительность',
        user_owner=u'Владелец',
        created=u'Дата создания',
        type_=u'Тип',
        access=u'Доступ',
        access_type=u'Тип доступа',
    )

    form_overrides = dict(
        type_=fields.Select2Field,
        access_type=fields.Select2Field,
    )

    column_choices = dict(
        type_=APP_MEDIA_TYPE,
        access_type=APP_MEDIA_LIST,
    )

    form_args = dict(
        type_=dict(
            choices=APP_MEDIA_TYPE,
        ),
        access_type=dict(
            choices=APP_MEDIA_LIST,
        ),
    )