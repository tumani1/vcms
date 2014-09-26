# coding: utf-8
import time

from models.users import UsersStream, Users
from models.media import Media
from models.comments import Comments
from models.persons import Persons
from models.mongo import constant
from utils.serializer import DefaultSerializer
from api.serializers.m_users_short import mUserShort
from api.serializers.m_attach import mAttach
from api.serializers.m_media import mMediaSerializer
from api.serializers.m_comment import mCommentSerializer
from api.serializers.m_persons import mPersonSerializer


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
        super(mStraemElement, self).__init__(**kwargs)
        if user is None:
            del self.fields['relation']

    def transform_created(self, obj):
        return obj.unixtime

    def transform_user(self, obj):
        ret_value = {}
        user = self.session.query(Users).get(obj.user_id)
        if user:
            ret_value = mUserShort(instance=obj, session=self.session, user=self.user).data
        return ret_value

    def transform_attach(self, obj):
        if obj.type == constant.APP_STREAM_TYPE_PERS_O:
            person = self.session.query(Persons).get(obj.object['person_id'])
            return mAttach(instance=person, type=constant.APP_STREAM_TYPE_PERS_O, session=self.session, user=self.user).data

    def transform_relation(self, obj):
        liked = None
        if self.user:
            user_str_el = self.session.query(UsersStream).get((obj.id, self.user.id))
            if user_str_el:
                liked = time.mktime(user_str_el.liked.timetuple())

        return {'liked': liked}

    def transform_object(self, obj):
        if obj.type in (constant.APP_STREAM_TYPE_USER_A, constant.APP_STREAM_TYPE_USER_F):
            user = self.session.query(Users).get(obj.user_id)
            partner = self.session.query(Users).get(obj.object['partner_id'])
            return mUserShort(instance=user, user=partner, session=self.session).data

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
            return mMediaSerializer(instance=media, session=self.session).data

        else:
            return {}