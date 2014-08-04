# coding: utf-8

from api.serializers import mStraemElement

from utils.validation import validate_mLimitId
from utils.exceptions import RequestErrorException

from models.mongo import Stream


def get(id, auth_user, session, **kwargs):
    try:
        stream_el = Stream.objects.filter(user_id=id)
        if 'type' in kwargs:
            stream_el = stream_el.filter(type=kwargs['type'])

        if 'limit' in kwargs:
            limit = validate_mLimitId(kwargs['limit'])
            stream_el = Stream.mLimitId(stream_el, limit)
            return mStraemElement(instance=stream_el, user=auth_user, session=session).data
    except Exception as e:
        raise RequestErrorException(e)

