# coding: utf-8

import os

from flask.ext.admin.model.template import macro

from admin.views.base import SqlAlModelView
from admin.fields import ImageUploadField, SelectField

from models.extras import Extras
from models.extras.constants import APP_EXTRA_TYPE
from settings import UPLOAD_DIR


def prefix_name(obj, file_data):
    return "poster.jpg"


class ExtrasModelView(SqlAlModelView):
    model = Extras
    category = u'Дополнительно'
    name = u'Дополнительные материалы'

    # inline_models = ((ExtrasMedia, dict(form_columns=['media_id', 'extra_type'])), )

    list_template = 'extras/list.html'

    column_list = (
        'id', 'cdn', 'title', 'title_orig', 'type',
        'location', 'created', 'description',
    )

    column_formatters = dict(location=macro('render_as_image'))
    column_display_pk = True

    column_choices = dict(
        type=APP_EXTRA_TYPE,
    )

    column_labels = dict(
        title=u'Название',
        type=u'Тип',
        location=u'Локация',
        title_orig=u'Оригинальное название',
        created=u'Дата создания',
        description=u'Описание',
    )

    form_columns = (
        'cdn', 'title', 'title_orig', 'type',
        'location', 'created', 'description',
    )

    form_overrides = dict(
        type=SelectField,
        location=ImageUploadField,
    )

    form_args = dict(
        type=dict(
            choices=APP_EXTRA_TYPE
        ),
        location=dict(
            base_path=os.path.join(UPLOAD_DIR, "p"),
            namegen=prefix_name,
            permission=0775
        ),
    )

    form_ajax_refs = dict(
        cdn={
            'fields': ('name',),
        },
    )

    def create_model(self, form):
        self.session.begin(subtransactions=True)
        try:
            return super(ExtrasModelView, self).create_model(form=form)
        except Exception as e:
            self.session.rollback()
            raise e

    def after_model_change(self, form, model, is_created):
        form.location._save_file(form.location.data, "{0}/{1}".format(model.id, model.location))
        self.session.commit()