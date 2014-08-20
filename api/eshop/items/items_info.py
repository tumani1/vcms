# coding: utf-8
from utils.validation import validate_int
from models.eshop.items.items import Items
from api.serializers.m_shop_item import mShopItem


def get(item_id, auth_user, session, **kwargs):
    data = {}
    item_id = validate_int(item_id, min_value=1)
    instance = Items.get_item_by_id(auth_user, session, item_id)
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mShopItem(**params).data
    return data