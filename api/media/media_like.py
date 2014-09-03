# coding: utf-8
import datetime

from models.mongo import Stream, constant
from models.media.media import Media
from models.media.users_media import UsersMedia
from utils import need_authorization
from utils.common import datetime_to_unixtime as convert_date


@need_authorization
def get(media_id, auth_user, session, **kwargs):
    data = {'liked': 0}
    users_media = Media.get_users_media_by_media(auth_user, session, media_id)
    if users_media:
        liked = convert_date(users_media.liked) if users_media.liked else 0
        data.update(liked=liked)
        return data
    return data


@need_authorization
def post(media_id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, media_id)
    date = datetime.datetime.utcnow()
    if users_media is None:
        users_media = UsersMedia(user_id=auth_user.id, media_id=media_id, liked=date)
        Stream.signal(type_=constant.APP_STREAM_TYPE_MEDIA_L, object_={'media_id': media_id}, user_id=auth_user.id)
        session.add(users_media)
    elif users_media.liked is None:
        users_media.liked = date
        Stream.signal(type_=constant.APP_STREAM_TYPE_MEDIA_L, object_={'media_id': media_id}, user_id=auth_user.id)
    if session.new or session.dirty:
        session.commit()


@need_authorization
def delete(media_id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, media_id)
    if not users_media is None:
        users_media.liked = None
    if session.dirty:
        session.commit()
