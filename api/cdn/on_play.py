# coding: utf-8
from models.media import Media, UsersMedia
from models.media.constants import APP_ACCESS_LEVEL_DEFAULT,\
    APP_ACCESS_LEVEL_MANAGER_MASK, APP_ACCESS_LEVEL_OWNER_MASK,\
    APP_ACCESS_LEVEL_GUEST_MASK, APP_ACCESS_LEVEL_AUTH_USER_MASK, APP_MEDIA_TYPE_PICTURE
from utils.exceptions import RequestErrorException
from utils.common import get_or_create
from utils.constants import HTTP_OK, HTTP_FORBIDDEN

from datetime import datetime


def get(auth_user, session, query, **kwargs):
    if 'media_id' in query:
        media = session.query(Media).get(query['media_id'])
    else:
        raise RequestErrorException
    if media is None:
        raise RequestErrorException

    access = media.access_level

    # TODO: media-unit
    if access is None:
        pass

    if access is None:
        access = media.media_type.access

    if access is None:
        access = int(APP_ACCESS_LEVEL_DEFAULT, 2)

    status_code = HTTP_FORBIDDEN
    if auth_user:
        if auth_user == media.user_owner and (access & APP_ACCESS_LEVEL_OWNER_MASK) != 0:
            status_code = HTTP_OK
        elif auth_user.is_manager and (access & APP_ACCESS_LEVEL_MANAGER_MASK) != 0:
            status_code = HTTP_OK
        elif (access & APP_ACCESS_LEVEL_AUTH_USER_MASK) != 0:
            status_code = HTTP_OK
    elif (access & APP_ACCESS_LEVEL_GUEST_MASK) != 0:
        status_code = HTTP_OK

    if status_code == HTTP_OK:
        if media.media_type.type_.code == APP_MEDIA_TYPE_PICTURE:
            media.views_cnt += 1

            if auth_user:
                users_media = get_or_create(session=session, model=UsersMedia,
                                            filter={'media_id': media.id, 'user_id': auth_user.id},
                                            create={'media_id': media.id, 'user_id': auth_user.id, 'views_cnt': 0})[0]
                users_media.watched = datetime.utcnow()
                users_media.views_cnt += 1

            session.commit()

    return status_code