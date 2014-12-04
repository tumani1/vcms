# coding: utf-8

from sqlalchemy.sql.functions import concat

from admin.fields import select_factory
from admin.validators import StreamUserTypeValidator
from admin.views.base import MongoDBModelView
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
        created=u'Дата создания', type=u'Тип', text=u'Техт',
        user_id=u'Пользователь', object=u'Объект')

    form_overrides = dict(
        user_id=select_factory(coerce=int, allow_blank=True, blank_text=u'Без пользователя'),
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
