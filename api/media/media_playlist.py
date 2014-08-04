# coding: utf-8
import datetime
from models.media.media import Media
from models.media.users_media import UsersMedia
from utils.date_converter import detetime_to_unixtime as convert_date


def get(id, auth_user, session, **kwargs):
    data = {'in_playlist': 0}
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if users_media:
        in_playlist = convert_date(users_media.playlist) if users_media.playlist else 0
        data.update(in_playlist=in_playlist)
        return data
    return data


def post(id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    date = datetime.datetime.utcnow()
    if users_media is None:
        users_media = UsersMedia(user_id=auth_user.id, media_id=id, playlist=date)
        session.add(users_media)
    elif users_media.playlist is None:
        users_media.playlist = date
    if session.new or session.dirty:
        session.commit()


def delete(id, auth_user, session, **kwargs):
    users_media = Media.get_users_media_by_media(auth_user, session, id)
    if not users_media is None:
        users_media.playlist = None
    if session.dirty:
        session.commit()