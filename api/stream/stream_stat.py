# coding: utf-8
import datetime

from models.mongo import Stream
from utils import need_authorization


@need_authorization
def get(auth_user, session, **kwargs):
    stream_object_count = Stream.objects(date__qte=auth_user.checked_stream, user_id=auth_user.id).count()
    auth_user.checked_stream = datetime.datetime.utcnow()
    session.commit()
    return stream_object_count