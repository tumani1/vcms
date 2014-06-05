# coding: utf-8

from models import dbWrap, UsersRels


@dbWrap
def get(user_id, partner_id,session = None):
    statuses = session.query(UsersRels.urStatus).filter_by(user_id=user_id, partner_id=partner_id)[0]
    return statuses
