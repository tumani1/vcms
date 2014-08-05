# coding: utf-8
from models.media import Media
from utils.exceptions import RequestErrorException


def get(auth_user, session, media_id, **kwargs):
    media = session.query(Media).get(media_id)
    if media is None:
        raise RequestErrorException
    access = media.media_locations.access
