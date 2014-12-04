# coding: utf-8

from wtforms.validators import ValidationError

from models.mongo.constant import APP_STREAM_TYPE_WITHOUT_USER


class StreamUserTypeValidator(object):

    def __init__(self, fieldname, message=u''):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data is None and other.data not in APP_STREAM_TYPE_WITHOUT_USER:
            raise ValidationError(self.message)
        elif field.data is not None and other.data in APP_STREAM_TYPE_WITHOUT_USER:
            raise ValidationError(self.message)