# coding: utf-8
from utils.validation import validate_mLimitId
from utils.exceptions import RequestErrorException
from api.stream.serizalizer import mStraemElement
from models.mongo import Stream


def get(auth_user, session, id, **kwargs):
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

