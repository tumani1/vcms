# coding: utf-8
import time

from models.users import UsersStream, Users
from models.media import Media
from models.mongo import constant
from utils.serializer import DefaultSerializer
from api.serializers import mUserShort, mAttach, mMediaSerializer


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

    def transform_id(self, obj):
        return obj.id

    def transform_user(self, obj):
        ret_value = {}
        user = self.session.query(Users).get(obj.user_id)
        if user:
            ret_value = mUserShort(instance=obj, session=self.session, user=self.user)
        return ret_value

    def transform_attach(self, obj):
        return mAttach(instance=obj, user=self.user, session=self.session)

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
            return mUserShort(instance=user, user=partner, session=self.session)

        if obj.type == constant.APP_STREAM_TYPE_MEDIA_L:
            user = self.session.query(Users).get(obj.user_id)
            media = self.session.query(Media).get(obj.object['media_id'])
            return mMediaSerializer(instance=media, user=user, session=self.session)
