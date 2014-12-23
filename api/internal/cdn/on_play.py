# coding: utf-8

from datetime import datetime

from models.media import Media, UsersMedia
from models.media.constants import APP_MEDIA_TYPE_PICTURE, APP_MEDIA_ACCESS_LIST

from common import access

from utils.common import get_or_create
from utils.exceptions import APIException, RequestErrorException
from utils.constants import HTTP_OK, HTTP_INTERNAL_SERVER_ERROR


def get(auth_user, session, query_params, reader, **kwargs):
    if 'media_id' in query_params and 'ip_address' in query_params:
        media_id = query_params['media_id']
    else:
        raise RequestErrorException

    media = session.query(Media).get(media_id)
    if media is None:
        raise RequestErrorException

    try:
        status_code = access(auth_user, query_params['ip_address'], media, session, reader)

    except APIException, e:
        status_code = e.code

    except Exception, e:
        if media.access_type.code == APP_MEDIA_ACCESS_LIST:
            status_code = HTTP_OK
        else:
            status_code = HTTP_INTERNAL_SERVER_ERROR

    if status_code == HTTP_OK:
        if media.type_.code == APP_MEDIA_TYPE_PICTURE:
            media.views_cnt += 1

            if auth_user:
                users_media = get_or_create(
                    session=session, model=UsersMedia,
                    filter={'media_id': media.id, 'user_id': auth_user.id},
                    create={'media_id': media.id, 'user_id': auth_user.id, 'views_cnt': 0}
                )[0]

                users_media.watched = datetime.utcnow()
                users_media.views_cnt += 1

            session.commit()

    return status_code
