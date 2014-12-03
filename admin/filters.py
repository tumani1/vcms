# coding: utf-8

from flask.ext.admin.contrib.sqla import filters


class ChoiceEqualFilter(filters.FilterEqual):

    def validate(self, value):
        return self.options and value in dict(self.options).keys()


class ChoiceNotEqualFilter(filters.FilterNotEqual):

    def validate(self, value):
        return self.options and value in dict(self.options).keys()


class IsPersonFilterEqual(ChoiceEqualFilter):

    def __init__(self, join_table, *args, **kwargs):
        self.join_method = join_table
        super(IsPersonFilterEqual, self).__init__(*args, **kwargs)

    def apply(self, query, value):
        return self.join_method(query=query)

class PhoneFilter(filters.FilterLike):
    pass
