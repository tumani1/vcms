# coding: utf-8
from api.serializers import mStreamElement

from utils.validation import validate_mLimitId
from utils.exceptions import RequestErrorException

from models.mongo import Stream


def get(user_id, auth_user, session, query, **kwargs):
    try:
        stream_el = Stream.objects.filter(user_id=user_id)
        if 'type' in query:
            stream_el = stream_el.filter(type=query['type'])

        if 'limit' in query:
            limit = validate_mLimitId(query['limit'])
            stream_el = Stream.mLimitId(stream_el, limit)
            return mStreamElement(instance=stream_el, user=auth_user, session=session).data

    except Exception as e:
        raise RequestErrorException(e)

