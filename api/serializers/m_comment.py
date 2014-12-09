# coding: utf-8
from sqlalchemy import and_

from models.users import Users
from models import Topics
from models import News
from models.comments import UsersComments
from models.media import MediaUnits, Media
from models.persons import Persons
from models.content import Content
from models.mongo import Stream

from api import serializers

from utils.common import datetime_to_unixtime as convert_date
from utils.serializer import DefaultSerializer

__all__ = ['mCommentSerializer']


class mCommentSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'user': '',
        'text': '',
        'object': '',
        'relation': '',
    }

    def __init__(self, **kwargs):
        self.object_types = {
            'mu': (MediaUnits, serializers.mMediaUnitsSerializer),
            'm': (Media, serializers.mMediaSerializer),
            'p': (Persons, serializers.mPersonSerializer),
            'c': (Content, serializers.mContentSerializer),
            's': (Stream, serializers.mStreamElement),
            't': (Topics, serializers.mTopicSerializer),
            'n': (News, serializers.mNewsSerializer)
        }
        self.with_obj = kwargs['with_obj'] if 'with_obj' in kwargs else False
        self.fields = self.__read_fields
        super(mCommentSerializer, self).__init__(**kwargs)
        self.users_ids, self.comment_ids = self.get_users_and_comment_ids_by_comments(self.instance)
        users = self.session.query(Users).filter(Users.id.in_(self.users_ids)).all()
        self.users_dict = dict()
        for user in users:
            self.users_dict[user.id] = user
        if self.is_auth:
            user_rel = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user.id, UsersComments.comment_id.in_(self.comment_ids))).all()
            self.rel_dict = dict()
            for ur in user_rel:
                self.rel_dict[ur.comment_id] = ur

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_user(self, instance, **kwargs):
        if instance.user_id in self.users_dict.keys():
            return serializers.mUserShort(user=self.user, session=self.session, instance=self.users_dict[instance.user_id]).data
        else:
            return u'removed user'

    def transform_text(self, instance, **kwargs):
        return instance.text

    def transform_object(self, instance, **kwargs):
        if self.with_obj:

            if instance.obj_id:
                if instance.obj_type.code == 's':
                    obj = self.object_types[instance.obj_type.code][0].objects.get(id=instance.obj_id)
                else:
                    obj = self.session.query(self.object_types[instance.obj_type.code][0]).filter_by(id=instance.obj_id).first()
            else:
                obj = self.session.query(self.object_types[instance.obj_type.code][0]).filter_by(name=instance.obj_id).first()
            if instance.obj_type.code == 'c':
                return self.object_types[instance.obj_type.code][1](obj).get_data()
            else:
                params = {
                    'instance': obj,
                    'user': self.user,
                    'session': self.session,
                }
                return self.object_types[instance.obj_type.code][1](**params).data

    def transform_relation(self, instance, **kwargs):
        relation = {}
        if instance.id in self.rel_dict.keys():
            if self.rel_dict[instance.id].liked:
                relation = {'liked': convert_date(self.rel_dict[instance.id].liked)}
        return relation

    def get_users_and_comment_ids_by_comments(self, comments):
        users_ids = []
        com_ids = []
        if not isinstance(comments, list):
            comments = [comments]
        for com in comments:
            users_ids.append(com.user_id)
            com_ids.append(com.id)
        return users_ids, com_ids
