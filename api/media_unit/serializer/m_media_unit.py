# coding: utf-8

from utils.serializer import DefaultSerializer


__all__ = ['mMediaUnitsSerializer']


class mMediaUnitsSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'title': '',
        'title_orig': '',
        'description': '',
        'releasedate': '',
        'enddate': '',
        'batch': '',
        'prev': '',
        'next': '',
        'relation': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mMediaUnitsSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_title(self, instance, **kwargs):
        return instance.title

    def transform_title_orig(self, instance, **kwargs):
        return instance.title_orig

    def transform_description(self, instance, **kwargs):
        return instance.description

    def transform_releasedate(self, instance, **kwargs):
        return instance.release_date

    def transform_enddate(self, instance, **kwargs):
        return instance.end_date

    def transform_batch(self, instance, **kwargs):
        return instance.batch

    def transform_prev(self, instance, **kwargs):
        return instance.previous_unit

    def transform_next(self, instance, **kwargs):
        return instance.next_unit

    def transform_relation(self, instance, **kwargs):
        relation = {}
        user_media_unit = instance.user_media_units
        if self.is_auth and not user_media_unit is None:
            if user_media_unit.subscribed:
                relation.update(subscribed=user_media_unit.subscribed)
            if user_media_unit.watched:
                relation.update(watched=user_media_unit.watched)
        return relation