# coding: utf-8

from flask.ext.admin.contrib.sqla import filters


class ChoiceEqualFilter(filters.FilterEqual):

    def validate(self, value):
        return self.options and value in dict(self.options).keys()


class ChoiceNotEqualFilter(filters.FilterNotEqual):

    def validate(self, value):
        return self.options and value in dict(self.options).keys()
