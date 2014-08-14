# coding: utf-8
from models.media import Media, UsersMedia
from models.media.constants import APP_MEDIA_TYPE_PICTURE, APP_MEDIA_ACCESS_LIST
from utils.exceptions import RequestErrorException
from utils.common import get_or_create
from api.cdn.common import access
from utils.exceptions import APIException
from utils.constants import HTTP_OK, HTTP_INTERNAL_SERVER_ERROR

from datetime import datetime


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

    if status_code == HTTP_OK:
        if media.type_.code == APP_MEDIA_TYPE_PICTURE:
            media.views_cnt += 1

            if auth_user:
                users_media = get_or_create(session=session, model=UsersMedia,
                                            filter={'media_id': media.id, 'user_id': auth_user.id},
                                            create={'media_id': media.id, 'user_id': auth_user.id, 'views_cnt': 0})[0]
                users_media.watched = datetime.utcnow()
                users_media.views_cnt += 1

            session.commit()

    return status_code