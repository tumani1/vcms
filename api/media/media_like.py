# coding: utf-8
import datetime
from models.media.media import Media
from models.media.users_media import UsersMedia
from utils.common import datetime_to_unixtime as convert_date


def get(media_id, auth_user, session, **kwargs):
    data = {'liked': 0}
    users_media = Media.get_users_media_by_media(auth_user, session, media_id)
    if users_media:
        liked = convert_date(users_media.liked) if users_media.liked else 0
        data.update(liked=liked)
        return data
    return data


def post(media_id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, media_id)
    date = datetime.datetime.utcnow()
    if users_media is None:
        users_media = UsersMedia(user_id=auth_user.id, media_id=media_id, liked=date)
        session.add(users_media)
    elif users_media.liked is None:
        users_media.liked = date
    if session.new or session.dirty:
        session.commit()


def delete(media_id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, media_id)
    if not users_media is None:
        users_media.liked = None
    if session.dirty:
        session.commit()
