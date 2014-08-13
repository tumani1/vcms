# coding: utf-8
from models.media import Media, UsersMedia
from models.media.constants import APP_MEDIA_TYPE_PICTURE
from utils.exceptions import RequestErrorException
from utils.common import get_or_create
from utils.constants import HTTP_OK
from api.cdn.common import access

from datetime import datetime


def get(auth_user, session, query, **kwargs):
    if 'media_id' in query and 'ip_address' in query:
        media = session.query(Media).get(query['media_id'])
    else:
        raise RequestErrorException
    if media is None:
        raise RequestErrorException

    status_code = access(auth_user, query['ip_address'], media, session)

    if status_code == HTTP_OK:
        if media.type_ == APP_MEDIA_TYPE_PICTURE:
            media.views_cnt += 1

            if auth_user:
                users_media = get_or_create(session=session, model=UsersMedia,
                                            filter={'media_id': media.id, 'user_id': auth_user.id},
                                            create={'media_id': media.id, 'user_id': auth_user.id, 'views_cnt': 0})[0]
                users_media.watched = datetime.utcnow()
                users_media.views_cnt += 1

            session.commit()

    return status_code