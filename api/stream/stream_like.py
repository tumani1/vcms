# coding: utf-8
from utils import need_authorization
from models.users import UsersStream


@need_authorization
def get(id, auth_user, session, **kwargs):
    unixtime = 0
    stream_el = session.query(UsersStream).filter_by(user_id=auth_user.id, stream_id=id)
    if stream_el:
        unixtime = stream_el.unixtime

    return unixtime


@need_authorization
def post(id, auth_user, session, **kwargs):
    stream_el = UsersStream(user_id=auth_user.id, stream_id=id)
    session.add(stream_el)
    session.commit()


@need_authorization
def delete(id, auth_user, session, **kwargs):
    stream_el = session.query(UsersStream).filter_by(user_id=auth_user.id, stream_id=id).delete()
    session.commit()