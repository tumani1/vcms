# coding: utf-8

from sqlalchemy.sql.functions import concat

from admin.validators import StreamUserTypeValidator
from admin.views.base import MongoDBModelView
from admin.fields import CKTextAreaField, select_factory

from models.users import Users
from models.mongo.stream import Stream

from utils.connection import get_session


class StreamModelView(MongoDBModelView):
    model = Stream
    name = u'Поток'
    category = u'Поток'
    session = get_session()

    users = list(session.query(Users.id, concat(Users.firstname, ' ', Users.lastname)).all())

    object_id_converter = int
    form_excluded_columns = ('id', )

    column_labels = dict(
        type=u'Тип', text=u'Техт', object=u'Объект',
        user_id=u'Пользователь')

    form_columns = ('user_id', 'type', 'object', 'attachments', 'text')

    form_overrides = dict(
        user_id=select_factory(coerce=int, allow_blank=True, blank_text=u'Без пользователя'),
        text=CKTextAreaField,
    )

    column_choices = dict(
        user_id=users
    )

    form_args = dict(
        user_id=dict(
            choices=users,
            validators=[StreamUserTypeValidator('type', message=u'Неверно выбран пользователь'), ],
        )
    )
