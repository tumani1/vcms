# coding: utf-8

from functools import partial

from flask.ext.admin.form.fields import Select2Field


def factory(*args, **kwargs):
    return partial(Select2Field, *args, **kwargs)