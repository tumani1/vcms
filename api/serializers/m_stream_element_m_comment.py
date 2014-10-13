# coding: utf-8
import time
from sqlalchemy import and_

from models.users import UsersStream, Users
from models.media import Media, MediaUnits
from models.comments import Comments, UsersComments
from models.persons import Persons
from models.content import Content
from models.mongo import constant, Stream
from utils.serializer import DefaultSerializer
from api.serializers.m_users_short import mUserShort
from api.serializers.m_attach import mAttach
from api.serializers.m_media import mMediaSerializer
from api.serializers.m_persons import mPersonSerializer
from api.serializers.m_media_unit import mMediaUnitsSerializer
from api.serializers.m_content import mContentSerializer
from utils.common import datetime_to_unixtime as convert_date


class mStraemElement(DefaultSerializer):

    __read_fields = {
        'id': '',
        'user': '',
        'created': '',
        'type': '',
        'object': '',
        'text': '',
        'attach': '',
        'relation': '',
    }

    def __init__(self, user=None, **kwargs):
        super(mStraemElement, self).__init__(user=user, **kwargs)
        if user is None:
            del self.fields['relation']

    def transform_created(self, obj):
        return convert_date(obj.created)

    def transform_user(self, obj):
        ret_value = {}
        user = None
        if not obj.user_id is None:
            user = self.session.query(Users).get(obj.user_id)
        if user:
            ret_value = mUserShort(instance=user, session=self.session, user=self.user).data
        return ret_value

    def transform_attach(self, obj):
        if obj.type == constant.APP_STREAM_TYPE_PERS_O:
            person = self.session.query(Persons).get(obj.attachments['person_id'])
            return mAttach(instance=person, type=constant.APP_STREAM_TYPE_PERS_O, session=self.session, user=self.user).data
        else:
            return {}

    def transform_relation(self, obj):
        liked = None
        if self.user:
            user_str_el = self.session.query(UsersStream).filter_by(stream_id=obj.id, user_id=self.user.id).first()
            if user_str_el:
                liked = convert_date(user_str_el.liked)

        return {'liked': liked}

    def transform_object(self, obj):
        if obj.type in (constant.APP_STREAM_TYPE_USER_A, constant.APP_STREAM_TYPE_USER_F):
            user = self.session.query(Users).get(obj.user_id)
            partner = self.session.query(Users).get(obj.object['partner_id'])
            return mUserShort(instance=partner, user=user, session=self.session).data

        elif obj.type == constant.APP_STREAM_TYPE_MEDIA_L:
            user = self.session.query(Users).get(obj.user_id)
            media = self.session.query(Media).get(obj.object['media_id'])
            return mMediaSerializer(instance=media, user=user, session=self.session).data

        elif obj.type == constant.APP_STREAM_TYPE_MEDIA_C:
            user = self.session.query(Users).get(obj.user_id)
            comment = self.session.query(Comments).get(obj.object['comment_id'])
            return mCommentSerializer(instance=comment, user=user, session=self.session, with_obj=True).data

        elif obj.type == constant.APP_STREAM_TYPE_PERS_S:
            user = self.session.query(Users).get(obj.user_id)
            person = self.session.query(Persons).get(obj.object['person_id'])
            return mPersonSerializer(instance=person, user=user, session=self.session).data

        elif obj.type == constant.APP_STREAM_TYPE_PERS_O:
            media = self.session.query(Media).get(obj.object['media_id'])
            return mMediaSerializer(instance=media, user=self.user, session=self.session).data

        else:
            return {}


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
            'mu': (MediaUnits, mMediaUnitsSerializer),
            'm': (Media, mMediaSerializer),
            'p': (Persons, mPersonSerializer),
            'c': (Content, mContentSerializer),
            's': (Stream, mStraemElement),
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
            return mUserShort(user=self.user, session=self.session, instance=self.users_dict[instance.user_id]).data
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
