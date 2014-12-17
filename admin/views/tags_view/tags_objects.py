# coding: utf-8

from admin.fields import SelectField
from admin.views.base import SqlAlModelView
from utils.constants import OBJECT_TYPES
from models.tags.tags_objects import TagsObjects


class TagsObjectsModelView(SqlAlModelView):
    model = TagsObjects
    category = u'Тэги'
    name = u'Отношение тэгов и объектов'

    column_list = form_columns = ('tag', 'obj_type', 'obj_id', 'obj_name')
    column_labels = dict(
        tag=u'Идентификатор тэга',
        obj_type=u'Тип объекта',
        obj_id=u'Идентификатор объекта',
        obj_name=u'Название объекта',
    )

    form_overrides = dict(
        obj_type=SelectField,
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        ),
    )



