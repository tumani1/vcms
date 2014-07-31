# coding: utf-8
from models import UsersRels
from models.users.constants import APP_USERSRELS_BLOCK_TYPE_UNDEF, APP_USERSRELS_BLOCK_TYPE_SEND,\
    APP_USERSRELS_BLOCK_TYPE_RECIEVE, APP_USERSRELS_BLOCK_TYPE_MATUALLY
from utils import need_authorization


@need_authorization
def post(auth_user, session, id, **kwargs):
    user_rels = session.query(UsersRels).filter_by(user_id=auth_user.id, partner_id=id).first()
    partner_rels = session.query(UsersRels).filter_by(user_id=id, partner_id=auth_user.id).first()
    if user_rels and partner_rels:
        if partner_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_SEND or user_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_RECIEVE:
            user_rels.blocked = APP_USERSRELS_BLOCK_TYPE_MATUALLY
            partner_rels.blocked = APP_USERSRELS_BLOCK_TYPE_MATUALLY
        elif partner_rels.blocked.code == user_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_UNDEF or user_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_SEND:
            user_rels.blocked = APP_USERSRELS_BLOCK_TYPE_SEND
            partner_rels.blocked = APP_USERSRELS_BLOCK_TYPE_RECIEVE
    else:
        user_rels = UsersRels(user_id=auth_user.id, partner_id=id, blocked=APP_USERSRELS_BLOCK_TYPE_SEND)
        partner_rels = UsersRels(user_id=id, partner_id=auth_user.id, blocked=APP_USERSRELS_BLOCK_TYPE_RECIEVE)
        session.add_all(user_rels, partner_rels)
    session.commit()


@need_authorization
def delete(auth_user, session, id, **kwargs):
    user_rels = session.query(UsersRels).filter_by(user_id=auth_user.id, partner_id=id).first()
    partner_rels = session.query(UsersRels).filter_by(user_id=id, partner_id=auth_user.id).first()
    if user_rels and partner_rels:
        if user_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_SEND or partner_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_RECIEVE:
            user_rels.blocked = APP_USERSRELS_BLOCK_TYPE_UNDEF
            partner_rels.blocked = APP_USERSRELS_BLOCK_TYPE_UNDEF
        elif user_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_MATUALLY or partner_rels.blocked.code == APP_USERSRELS_BLOCK_TYPE_MATUALLY:
            user_rels.blocked = APP_USERSRELS_BLOCK_TYPE_RECIEVE
            partner_rels.blocked = APP_USERSRELS_BLOCK_TYPE_SEND
    session.commit()