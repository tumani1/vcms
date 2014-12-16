# coding: utf-8

from flask.ext.admin.contrib.sqla import filters

from models.media import MediaInUnit


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


class MediaUnitFilter(filters.FilterInList):
    def apply(self, query, value):
        return query.join(MediaInUnit).filter(MediaInUnit.media_unit_id.in_(value))


class PhoneFilter(filters.FilterLike):
    pass
