# coding: utf-8
from api.serializers.m_extra import mExtra
from utils.validation import validate_int
from models.eshop.variants.variants import Variants
from models.eshop.items.items import Items


def get(item_id, auth_user, session, **kwargs):
    data = {}
    item_id = validate_int(item_id, min_value=1)
    if 'variant' in kwargs['query_params']:
        variant_id = validate_int(kwargs['query_params']['variant'], min_value=1)
        instance = Variants.get_variant_extras(session, variant_id)
    else:
        instance = Items.get_item_extras(session, item_id)

    if not instance is None:
        serializer_params = {
            'user': auth_user,
            'session': session,
            'instance': instance.all(),
        }
        data = mExtra(**serializer_params).data
    return data