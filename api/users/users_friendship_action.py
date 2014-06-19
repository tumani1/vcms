# coding: utf-8
from models import UsersRels
from db_engine import db
from models.users.constants import APP_USERSRELS_TYPE_UNDEF, APP_USERSRELS_TYPE_FRIEND,\
    APP_USERSRELS_TYPE_SEND_TO, APP_USERSRELS_TYPE_RECIEVE_USER
from utils import need_authorization


@db
@need_authorization
def get(auth_user, id, session=None, *args, **kwargs):
    status = session.query(UsersRels.urStatus).filter_by(user_id=auth_user, partner_id=id).first()[0]
    if status:
        return status.code
    else:
        return APP_USERSRELS_TYPE_UNDEF


@db
@need_authorization
def post(auth_user, id, session=None, *args, **kwargs):
    user_rels = session.query(UsersRels).filter_by(user_id=auth_user.id, partner_id=id).first()
    partner_rels = session.query(UsersRels).filter_by(user_id=id, partner_id=auth_user.id).first()
    if user_rels and partner_rels:
        if partner_rels.urStatus == user_rels.urStatus.code == APP_USERSRELS_TYPE_UNDEF:
            user_rels.urStatus = APP_USERSRELS_TYPE_SEND_TO
            partner_rels.urStatus = APP_USERSRELS_TYPE_RECIEVE_USER
        else:
            user_rels.urStatus = partner_rels.urStatus = APP_USERSRELS_TYPE_FRIEND
    else:
        user_rels.urStatus = APP_USERSRELS_TYPE_SEND_TO
        partner_rels.urStatus = APP_USERSRELS_TYPE_RECIEVE_USER

    session.add_all(user_rels, partner_rels)
    session.commit()


@db
@need_authorization
def delete(auth_user, id, session=None, *args, **kwargs):
    rels = session.query(UsersRels).filter(((UsersRels.user_id == auth_user.id) &
                                            (UsersRels.partner_id == id))
                                           | ((UsersRels.user_id == id) &
                                              (UsersRels.partner_id == user)))
    for rel in rels:
        rel.urStatus = APP_USERSRELS_TYPE_UNDEF
    session.commit()