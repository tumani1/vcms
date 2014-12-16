# coding: utf-8

from wtforms import TextAreaField

from admin.widgets import CKTextAreaWidget


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()