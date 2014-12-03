# coding: utf-8
from utils.serializer import DefaultSerializer
from api.serializers.m_persons import mPersonSerializer
from models.mongo import constant

OBJECT_TYPE = {
    constant.APP_STREAM_TYPE_PERS_O: lambda instance, session, user: mPersonSerializer(instance=instance, user=user, session=session).data,
}


class mAttach(DefaultSerializer):

    __read_fields = {
        'type': '',
        'id': '',
        'id_str': '',
        'object': '',
    }

    def __init__(self, type=None, *args, **kwargs):
        self.type = type
        super(mAttach, self).__init__(*args, **kwargs)

    def transform_type(self, obj):
        return self.type

    def transform_id_str(self, obj):
        return str(obj.id)

    def transform_object(self, obj):
        try:
            return OBJECT_TYPE[self.type](instance=obj, session=self.session, user=self.user)
        except KeyError:
            return {}