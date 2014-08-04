# coding: utf-8

from api.serializers import mStraemElement

from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimitId
from models.mongo import Stream


def get(auth_user, session, **kwargs):
    query = kwargs['query']
    stream_el = Stream.objects.all()

    if 'type' in query and 'objects' in query:
        if 'objects' in query:
            types = [obj[0] for obj in query['objects']]
            ids = [obj[1] for obj in query['objects']]
            stream_el = stream_el.filter(type__in=types, id__in=ids)

        elif 'type' in query:
            types = type if isinstance(query['type'], list) else [query['type']]
            stream_el = stream_el.filter(type__in=types)

    if 'limit' in query:
        try:
            limit = validate_mLimitId(kwargs['limit'])
            stream_el = Stream.mLimitId(stream_el, limit)
        except Exception as e:
            raise RequestErrorException(e)

    return mStraemElement(instance=stream_el, user=auth_user, session=session).data

