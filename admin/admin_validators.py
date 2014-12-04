# coding: utf-8

import re

from wtforms.validators import ValidationError


def custom_phone_validator(form, field):
    template = r"^\+?1?\d{9,15}$"
    if re.compile(template).match(field.data) is None:
        raise ValidationError(u"Формат ввода: '+999999999'")


def custom_email_validator(form, field):
    template = r"^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])$"
    if re.compile(template).match(field.data) is None:
        raise ValidationError(u'Email не соответствует формату')
