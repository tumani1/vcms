# coding: utf-8

from api.serializers import mStraemElement

from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimitId
from models.mongo import Stream


def get(auth_user, session, **kwargs):
    stream_el = Stream.objects.all()
    if 'type' in kwargs and 'objects' in kwargs:
        if 'objects' in kwargs:
            types = [obj[0] for obj in kwargs['objects']]
            ids = [obj[1] for obj in kwargs['objects']]
            stream_el = stream_el.filter(type__in=types, id__in=ids)
        elif 'type' in kwargs:
            types = type if isinstance(kwargs['type'], list) else [kwargs['type']]
            stream_el = stream_el.filter(type__in=types)
    if 'limit' in kwargs:
        try:
            limit = validate_mLimitId(kwargs['limit'])
            stream_el = Stream.mLimitId(stream_el, limit)
        except Exception as e:
            raise RequestErrorException(e)

    return mStraemElement(instance=stream_el, user=auth_user, session=session).data

