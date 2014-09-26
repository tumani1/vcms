# coding: utf-8
import datetime

from models.mongo import Stream, constant
from models.media import MediaUnits, UsersMediaUnits
from utils import need_authorization
from utils.common import datetime_to_unixtime as convert_date


@need_authorization
def get(id, auth_user, session, **kwargs):
    data = {'liked': 0}
    users_media = MediaUnits.get_users_media_unit(auth_user, session, id)
    if users_media:
        liked = convert_date(users_media.liked) if users_media.liked else 0
        data.update(liked=liked)
        return data
    return data


@need_authorization
def post(id, auth_user, session, **kwargs):
    users_media = MediaUnits.get_users_media_unit(auth_user, session, id)
    date = datetime.datetime.utcnow()
    if users_media is None:
        users_media = UsersMediaUnits(user_id=auth_user.id, media_unit_id=id, liked=date)
        Stream.signal(type_=constant.APP_STREAM_TYPE_MUNIT_S, object_={'mediaunit_id': id}, user_id=auth_user.id)
        session.add(users_media)
    elif users_media.liked is None:
        users_media.liked = date
        Stream.signal(type_=constant.APP_STREAM_TYPE_MEDIA_L, object_={'mediaunit_id': id}, user_id=auth_user.id)
    if session.new or session.dirty:
        session.commit()


@need_authorization
def delete(id, auth_user, session, **kwargs):
    users_media = MediaUnits.get_users_media_unit(auth_user, session, id)
    if not users_media is None:
        users_media.liked = None
    if session.dirty:
        session.commit()
