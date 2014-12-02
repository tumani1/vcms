# coding: utf-8
from utils.serializer import DefaultSerializer
from utils.common import datetime_to_unixtime as convert_date, list_of
from api.serializers.m_localion import mLocationSerializer
from api.serializers.m_media_unit import mMediaUnitsSerializer

__all__ = ['mMediaSerializer']


class mMediaSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'title': '',
        'title_orig': '',
        'description': '',
        'releasedate': '',
        'duration': '',
        'relation': '',
        'views_cnt': '',
        'rating': '',
        'rating_votes': '',
        'locations': '',
        'units': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mMediaSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_title(self, instance, **kwargs):
        return instance.title

    def transform_title_orig(self, instance, **kwargs):
        return instance.title_orig

    def transform_description(self, instance, **kwargs):
        return instance.description

    def transform_releasedate(self, instance, **kwargs):
        if instance.release_date:
            return convert_date(instance.release_date)

    def transform_duration(self, instance, **kwargs):
        return instance.duration

    def transform_locations(self, instance, **kwargs):
        return mLocationSerializer(user=self.user, session=self.session, instance=instance.media_locations).data

    def transform_relation(self, instance, **kwargs):
        relation = {}
        users_media = instance.users_media_query.filter_by(users=self.user).first()
        if self.is_auth and not users_media is None:
            if users_media.watched:
                relation.update(watched=convert_date(users_media.watched))
            if users_media.liked:
                relation.update(liked=convert_date(users_media.liked))
            if users_media.play_pos:
                relation.update(pos=users_media.play_pos)
            if users_media.playlist:
                relation.update(playlist=users_media.play_pos)
            if users_media.rating:
                relation.update(rating=users_media.rating)
        return relation

    def transform_units(self, instance, **kwargs):
        units = list_of(instance.media_units, 'media_units', objects=True)
        return mMediaUnitsSerializer(user=self.user, session=self.session, instance=units, small=True).data

    def transform_views_cnt(self, instance, **kwargs):
        return instance.views_cnt

    def transform_rating(self, instance, **kwargs):
        return instance.rating

    def transform_rating_votes(self, instance, **kwargs):
        return instance.rating_votes