# coding: utf-8
import time

from utils.serializer import DefaultSerializer
from api.users.serializer import mUserShort
from models.users import UsersStream, Users


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
        return {}

    def transform_relation(self, obj):
        liked = None
        if self.user:
            user_str_el = self.session.query(UsersStream).get((obj.id, self.user.id))
            if user_str_el:
                liked = time.mktime(user_str_el.liked.timetuple())

        return {'liked': liked}
