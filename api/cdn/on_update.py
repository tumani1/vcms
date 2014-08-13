# coding: utf-8
from models.media import Media
from common import access
from utils.exceptions import RequestErrorException


def get(auth_user, session, query, **kwargs):
    if 'media_id' in query and 'ip_address' in query:
        media = session.query(Media).get(query['media_id'])
    else:
        raise RequestErrorException
    if media is None:
        raise RequestErrorException

    status_code = access(auth_user, query['ip_address'], media, session)
    return status_code