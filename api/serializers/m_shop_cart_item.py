# coding: utf-8
from api.serializers.m_shop_item import mShopItem
from models import Variants, Items
from utils.serializer import DefaultSerializer
from utils.common import datetime_to_unixtime as convert_date


class mShopCartItem(DefaultSerializer):

    __read_fields = {
        'id': '',
        'cart_id': '',
        'added': '',
        'cnt': '',
        'cost': '',
        'price': '',
        'item': '',
        'variant_id': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mShopCartItem, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_cart_id(self, instance, **kwargs):
        return instance.carts_id

    def transform_added(self, instance, **kwargs):
        if instance.added is None:
            return None
        return convert_date(instance.added)

    def transform_cnt(self, instance, **kwargs):
        return instance.cnt

    def transform_cost(self, instance, **kwargs):
        return instance.cost

    def transform_price(self, instance, **kwargs):
        return instance.price

    def transform_item(self, instance, **kwargs):
        variants = Variants.get_variants_by_id(self.session, instance.variant_id).first()
        items_instance = Items.get_item_by_id(self.user, self.session, variants.item_id)
        return mShopItem(instance=items_instance, user=self.user, session=self.session).data

    def transform_variant_id(self, instance, **kwargs):
        return instance.variant_id
