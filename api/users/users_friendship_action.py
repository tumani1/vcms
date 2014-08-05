# coding: utf-8
from models.users import UsersRels
from models.users.constants import APP_USERSRELS_TYPE_UNDEF, APP_USERSRELS_TYPE_FRIEND,\
    APP_USERSRELS_TYPE_SEND_TO, APP_USERSRELS_TYPE_RECIEVE_USER
from utils import need_authorization


@need_authorization
def get(user_id, auth_user, session, *args, **kwargs):
    status = session.query(UsersRels.urStatus).filter_by(user_id=auth_user.id, partner_id=user_id).first()
    if status:
        return status[0].code
    else:
        return APP_USERSRELS_TYPE_UNDEF


@need_authorization
def post(user_id, auth_user, session, *args, **kwargs):
    user_rels = session.query(UsersRels).filter_by(user_id=auth_user.id, partner_id=user_id).first()
    partner_rels = session.query(UsersRels).filter_by(user_id=user_id, partner_id=auth_user.id).first()

    if user_rels and partner_rels:
        if partner_rels.urStatus.code == user_rels.urStatus.code == APP_USERSRELS_TYPE_UNDEF:
            user_rels.urStatus = APP_USERSRELS_TYPE_SEND_TO
            partner_rels.urStatus = APP_USERSRELS_TYPE_RECIEVE_USER
        else:
            user_rels.urStatus = partner_rels.urStatus = APP_USERSRELS_TYPE_FRIEND
    else:
        user_rels = UsersRels(user_id=auth_user.id, partner_id=user_id, urStatus=APP_USERSRELS_TYPE_SEND_TO)
        partner_rels = UsersRels(user_id=user_id, partner_id=auth_user.id, urStatus=APP_USERSRELS_TYPE_RECIEVE_USER)
        session.add_all(user_rels, partner_rels)

    session.commit()


@need_authorization
def delete(user_id, auth_user, session, *args, **kwargs):
    user_rels = session.query(UsersRels).filter_by(user_id=auth_user.id, partner_id=user_id).first()
    partner_rels = session.query(UsersRels).filter_by(user_id=user_id, partner_id=auth_user.id).first()

    if user_rels and partner_rels:
        if user_rels.urStatus.code == APP_USERSRELS_TYPE_FRIEND and partner_rels.urStatus.code == APP_USERSRELS_TYPE_FRIEND:
            user_rels.urStatus = APP_USERSRELS_TYPE_UNDEF
            partner_rels.urStatus = APP_USERSRELS_TYPE_SEND_TO
        else:
            user_rels.urStatus = APP_USERSRELS_TYPE_UNDEF
            partner_rels.urStatus = APP_USERSRELS_TYPE_UNDEF
        session.commit()
