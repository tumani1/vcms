# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView


class ChatsModelView(ModelView):
    column_display_pk = True
    column_labels = dict(description=u'Дескриптор чата')

    form_excluded_columns = ('users_chat', )