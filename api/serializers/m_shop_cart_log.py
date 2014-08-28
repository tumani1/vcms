from utils.serializer import DefaultSerializer
from utils.common import datetime_to_unixtime as convert_date


class mShopCartLog(DefaultSerializer):

    __read_fields = {
        'id': '',
        'cart_id': '',
        'time': '',
        'status': '',
        'comment': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mShopCartLog, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_cart_id(self, instance, **kwargs):
        return instance.cart_id

    def transform_time(self, instance, **kwargs):
        if instance.time is None:
            return None
        return convert_date(instance.time)

    def transform_status(self, instance, **kwargs):
        return instance.status

    def transform_comment(self, instance, **kwargs):
        return instance.comment


