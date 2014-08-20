# coding: utf-8
from models.extras.extras import Extras
from api.serializers.m_extra import mExtra
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
        'extras': ''

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

    def transform_extras(self, instance, **kwargs):
        extras_ids = []
        for extra in instance.item_extras:
            extras_ids.append(extra.extras_id)
        extras_instance = self.session.query(Extras).filter(Extras.id.in_(extras_ids)).all()
        extras = mExtra(instance=extras_instance, user=self.user, session=self.session).data
        return extras

    def transform_relation(self, instance, **kwargs):
        relation = {}
        item_user = instance.item_users
        if self.is_auth and item_user:
            if item_user[0].watched:               # [0] тк как существует только один обект связи одного юнита и юзера
                relation.update(watched=convert_date(item_user[0].watched))
            if item_user[0].bought_cnt:
                relation.update(bought_cnt=item_user[0].bought_cnt)
            if item_user[0].wished:
                relation.update(wished=convert_date(item_user[0].wished))
        return relation