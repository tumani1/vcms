# coding: utf-8
from utils.validation import validate_int
from models.eshop.variants.variants import Variants
from api.serializers.m_shop_item_variants import mShopItemVariants


def get(item_id, auth_user, session, **kwargs):
    data = {}
    item_id = validate_int(item_id, min_value=1)
    instance = Variants.get_variants_by_item_id(session, item_id)
    if not instance is None:
        params = {
            'instance': instance.all(),
            'user': auth_user,
            'session': session,
        }
        data = mShopItemVariants(**params).data
    return data
