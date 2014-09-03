# coding: utf-8
from utils.common import datetime_to_unixtime
from api.serializers.m_users_short import mUserShort

__all__ = ['mUser']


class mUser(mUserShort):

    __read_fields = {
        'id': '',
        'firstname': '',
        'lastname': '',
        'gender': '',
        'regdate': '',
        'lastvisit': '',
        'is_online': '',
        'city': '',
        'country': '',
    }

    def transform_lastvisit(self, obj):
        return datetime_to_unixtime(obj.last_visit.timetuple()) if not obj.last_visit is None else ''

    def transform_regdate(self, obj):
        return datetime_to_unixtime(obj.created)

    def transform_city(self, obj):
        return obj.city.name

    def transform_country(self, obj):
        return obj.city.country.name

    def transform_gender(self, obj):
        return obj.gender.code
