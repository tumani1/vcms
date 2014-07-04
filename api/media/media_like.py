# coding: utf-8
import datetime
from models.media.media import Media
from models.media.users_media import UsersMedia
from utils.date_converter import detetime_to_unixtime as convert_date


def get(auth_user, session, id, **kwargs):
    data = {'liked': 0}
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if users_media:
        liked = convert_date(users_media.liked) if users_media.liked else 0
        data.update(liked=liked)
        return data
    return data


def post(auth_user, session, id, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    date = datetime.datetime.utcnow()
    if users_media is None:
        users_media = UsersMedia(user_id=auth_user.id, media_id=id, liked=date)
        session.add(users_media)
    elif users_media.liked is None:
        users_media.liked = date
    if session.new or session.dirty:
        session.commit()


def delete(auth_user, session, id, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if not users_media is None:
        users_media.liked = None
    if session.dirty:
        session.commit()