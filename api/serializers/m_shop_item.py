# coding: utf-8

from utils.serializer import DefaultSerializer
from utils.common import detetime_to_unixtime as convert_date

__all__ = ['mShopItem']


class mShopItem(DefaultSerializer):

    __read_fields = {
        'id': '',
        'name': '',
        'description': '',
        'instock': '',
        'is_digital': '',
        'price': '',
        'price_old': '',
        'relation': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mShopItem, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_name(self, instance, **kwargs):
        return instance.name

    def transform_instock(self, instance, **kwargs):
        return instance.instock

    def transform_description(self, instance, **kwargs):
        return instance.description

    def transform_is_digital(self, instance, **kwargs):
        return instance.is_digital

    def transform_price(self, instance, **kwargs):
        return instance.price

    def transform_price_old(self, instance, **kwargs):
        return instance.price_old

    def transform_relation(self, instance, **kwargs):
        pass