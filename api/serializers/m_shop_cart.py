# coding: utf-8
from api.serializers.m_shop_cart_item import mShopCartItem
from api.serializers.m_shop_cart_log import mShopCartLog
from utils.serializer import DefaultSerializer


class mShopCart(DefaultSerializer):

    __read_fields = {
        'id': '',
        'created': '',
        'status': '',
        'payed': '',
        'cost': '',
        'items': '',
        'log': '',
        'items_cnt': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mShopCart, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_created(self, instance, **kwargs):
        return instance.created

    def transform_status(self, instance, **kwargs):
        return instance.status

    def transform_payed(self, instance, **kwargs):
        return instance.payments[0].payed

    def transform_cost(self, instance, **kwargs):
        return instance.cost_total

    def transform_items(self, instance, **kwargs):
        items_carts_instance = instance.items_carts[0]

        return mShopCartItem(instance=items_carts_instance, user=self.user, session=self.session).data

    def transform_items_cnt(self, instance, **kwargs):
        return instance.items_cnt

    def transform_log(self, instance, **kwargs):
        log_instance = instance.log

        return mShopCartLog(instance=log_instance, user=self.user, session=self.session).data