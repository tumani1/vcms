# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import MongoDBModelView
from models.users import Users
from models.mongo.stream import Stream
from utils.connection import get_session


class StreamModelView(MongoDBModelView):
    model = Stream
    name = u'Поток'
    category = u'Поток'
    session = get_session()

    users = list(session.query(Users.id, Users).all())

    object_id_converter = int
    form_excluded_columns = ('id', )

    column_labels = dict(
        created=u'Дата создания', type=u'Тип', text=u'Техт',
        user_id=u'Пользователь', object=u'Объект')

    form_overrides = dict(
        user_id=fields.Select2Field,
    )

    column_choices = dict(
        user_id=users
    )

    form_args = dict(
        user_id=dict(
            choices=users
        )
    )
