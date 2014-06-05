# coding: utf-8
from models import db, UsersRels
from models.users.constants import APP_USERSRELS_TYPE_UNDEF, APP_USERSRELS_TYPE_FRIEND,\
    APP_USERSRELS_TYPE_SEND_TO, APP_USERSRELS_TYPE_FROM_USER
from utils import need_authorization


@db
@need_authorization
def get(user_id, partner_id, session=None, *args, **kwargs):
    status = session.query(UsersRels.urStatus).filter_by(user_id=user_id, partner_id=partner_id).first()[0]
    if status:
        return int(status.code)
    else:
        return int(APP_USERSRELS_TYPE_UNDEF)


@db
@need_authorization
def post(user_id, partner_id, status, session=None):
    if status in (APP_USERSRELS_TYPE_FRIEND, APP_USERSRELS_TYPE_UNDEF):
        if status == APP_USERSRELS_TYPE_FRIEND:
            user_rels = session.query(UsersRels).filter_by(user_id=user_id, partner_id=partner_id, urStatus=APP_USERSRELS_TYPE_FROM_USER).first()
            partner_rels = session.query(UsersRels).filter_by(user_id=partner_id, partner_id=user_id, urStatus=APP_USERSRELS_TYPE_SEND_TO).first()
        else:
            user_rels = session.query(UsersRels).filter_by(user_id=user_id, partner_id=partner_id).first()
            partner_rels = session.query(UsersRels).filter_by(user_id=partner_id, partner_id=user_id).first()
        if user_rels and partner_rels:
            user_rels.urStatus = partner_rels.urStatus = status
        else:
            raise ValueError("Not valid data")

    elif status == APP_USERSRELS_TYPE_SEND_TO:
        user_rels = session.query(UsersRels).filter_by(user_id=user_id, partner_id=partner_id).first()
        partner_rels = session.query(UsersRels).filter_by(user_id=partner_id, partner_id=user_id).first()
        if not user_rels:
            user_rels = UsersRels(user_id=user_id, partner_id=partner_id, urStatus=status)
            session.add(user_rels)
        else:
            user_rels.urStatus = status
        if not partner_rels:
            partner_rels = UsersRels(user_id=partner_id, partner_id=user_id, urStatus=APP_USERSRELS_TYPE_FROM_USER)
            session.add(partner_rels)
        else:
            partner_rels.urStatus = APP_USERSRELS_TYPE_FROM_USER
    else:
        raise ValueError("Not valid status")

    session.commit()


@db
@need_authorization
def delete(user_id, partner_id, session=None, *args, **kwargs):
    rels = session.query(UsersRels).filter(((UsersRels.user_id == user_id) &
                                            (UsersRels.partner_id == partner_id))
                                           | ((UsersRels.user_id == partner_id) &
                                              (UsersRels.partner_id == user_id)))
    for rel in rels:
        rel.urStatus = APP_USERSRELS_TYPE_UNDEF
    session.commit()


print get(1, 2)
post(1, 2, APP_USERSRELS_TYPE_SEND_TO)