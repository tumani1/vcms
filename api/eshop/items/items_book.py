# coding: utf-8
from sqlalchemy import and_
from utils import need_authorization
from utils.validation import validate_int
from models.eshop.variants.variants import Variants
from models.eshop.carts.carts import Carts
from models.eshop.carts.items_carts import ItemsCarts
import datetime


@need_authorization
def  post(item_id, auth_user, session, **kwargs):
    item_id = validate_int(item_id, min_value=1)
    date = datetime.datetime.utcnow()

    if 'variant' in kwargs['query_params']:
        variant_id = validate_int(kwargs['query_params']['variant'])
        variant = Variants.get_variants_by_id(session, variant_id).first()
        if variant.item_id != item_id:
            raise Exception("Неверный вариант!")
    else:
        variants = Variants.get_variants_by_item_id(session, item_id)
        if len(variants.all()) == 1:
            variant = variants.first()
        else:
            raise Exception("У элемента не один вариант!")

    cart = Carts.get_cart_by_user_id(session, auth_user.id).first()
    if cart is None:
        cart = Carts(user_id=auth_user.id, created=date, updated=date)
        session.add(cart)
        session.commit()
        cart = Carts.get_cart_by_user_id(session, auth_user.id).first()

    item_cart = session.query(ItemsCarts).filter(and_(ItemsCarts.carts_id == cart.id, ItemsCarts.variant_id == variant.id)).first()

    if item_cart is None:
        item_cart = ItemsCarts(carts_id=cart.id, variant_id=variant.id, cnt=1, price=variant.price, cost=variant.price, added=date)
        session.add(item_cart)
        session.commit()
    else:
        item_cart.cnt += 1
        item_cart.price = variant.price
        item_cart.cost = variant.price * item_cart.cnt

    if cart.items_cnt is None:
        cart.items_cnt = 1
    else:
        cart.items_cnt += 1

    if cart.cost_total is None:
        cart.cost_total = variant.price
    else:
        cart.cost_total += variant.price

    cart.updated = date

    session.commit()


def delete(item_id, auth_user, session, **kwargs):
    item_id = validate_int(item_id, min_value=1)
    date = datetime.datetime.utcnow()

    if 'variant' in kwargs['query_params']:
        variant_id = validate_int(kwargs['query_params']['variant'])
        variant = Variants.get_variants_by_id(session, variant_id).first()
        if variant.item_id != item_id:
            raise Exception("Неверный вариант!")
    else:
        variants = Variants.get_variants_by_item_id(session, item_id)
        if len(variants.all()) == 1:
            variant = variants.first()
        else:
            raise Exception("У элемента не один вариант!")

    cart = Carts.get_cart_by_user_id(session, auth_user.id).first()
    if cart is None:
        raise Exception("Пользователь еще ничего не добывлял в корзину!")

    item_cart = session.query(ItemsCarts).filter(and_(ItemsCarts.carts_id == cart.id, ItemsCarts.variant_id == variant.id)).first()

    if item_cart is None:
        raise Exception("Такого элемента нет в корзине!")

    if item_cart.cnt > 0:
        item_cart.cnt -= 1
        item_cart.cost -= variant.price
        cart.items_cnt -= 1
        cart.cost_total += variant.price
        cart.updated = date
        session.commit()
    else:
        raise Exception("Такого элемента нет в корзине!")