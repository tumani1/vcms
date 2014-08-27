from utils.serializer import DefaultSerializer


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
        return instance.time

    def transform_status(self, instance, **kwargs):
        return instance.status

    def transform_comment(self, instance, **kwargs):
        return instance.comment


