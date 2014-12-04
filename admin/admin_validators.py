# coding: utf-8

import re

from wtforms.validators import ValidationError


def custom_phone_validator(form, field):
    if re.compile(r'^\+?1?\d{9,15}$').match(field.data) is None:
        raise ValidationError(u"Формат ввода: '+999999999'")

