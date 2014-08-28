# coding: utf-8
from models.extras.extras import Extras
from api.serializers.m_extra import mExtra
from utils.serializer import DefaultSerializer

__all__ = ['mShopItemVariants']


class mShopItemVariants(DefaultSerializer):

    __read_fields = {
        'id': '',
        'item_id': '',
        'name': '',
        'description': '',
        'available_cnt': '',
        'price': '',
        'price_old': '',
        'extras': '',
        'values': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mShopItemVariants, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_name(self, instance, **kwargs):
        return instance.item_id

    def transform_instock(self, instance, **kwargs):
        return instance.name

    def transform_description(self, instance, **kwargs):
        return instance.description

    def transform_available_cnt(self, instance, **kwargs):
        return instance.stock_cnt - instance.reserved_cnt

    def transform_price(self, instance, **kwargs):
        return instance.price

    def transform_price_old(self, instance, **kwargs):
        return instance.price_old

    def transform_extras(self, instance, **kwargs):
        extras_ids = []
        for extra in instance.variant_extras:
            extras_ids.append(extra.extras_id)
        extras_instance = self.session.query(Extras).filter(Extras.id.in_(extras_ids)).all()
        extras = mExtra(instance=extras_instance, user=self.user, session=self.session).data
        return extras

    def transform_values(self, instance, **kwargs):
        values_list = []
        for val in instance.variant_values:
            values_list.append(dict(name=val.name, value=val.value))
        return  values_list