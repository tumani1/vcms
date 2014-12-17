# coding: utf-8

from flask.ext.admin.form.fields import Select2Field


class SelectField(Select2Field):
    def process_data(self, value):
        if value is None:
            self.data = None
        else:
            try:
                self.data = self.coerce(value.code)
            except (ValueError, TypeError):
                self.data = None