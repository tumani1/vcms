# coding: utf-8
from models.media import Media
from models.media.constants import APP_MEDIA_ACCESS_LIST
from common import access
from utils.exceptions import RequestErrorException, APIException
from utils.constants import HTTP_OK, HTTP_INTERNAL_SERVER_ERROR


def get(auth_user, session, query, reader, **kwargs):
    if 'media_id' in query and 'ip_address' in query:
        media_id = query['media_id']
    else:
        raise RequestErrorException
    media = session.query(Media).get(media_id)
    if media is None:
        raise RequestErrorException

    try:
        status_code = access(auth_user, query['ip_address'], media, session, reader)
    except APIException as e:
        status_code = e.code
    except Exception as e:
        if media.access_type.code == APP_MEDIA_ACCESS_LIST:
            status_code = HTTP_OK
        else:
            status_code = HTTP_INTERNAL_SERVER_ERROR
    return status_code