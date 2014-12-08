# coding: utf-8
from models.mongo import Stream
from api.serializers import mStreamElement

from utils.exceptions import RequestErrorException


def get(auth_user, id, session, **kwargs):
    try:
        stream_el = Stream.objects().get(id=int(id))
    except:
        raise RequestErrorException("Not valid id value")
    return mStreamElement(instance=stream_el, user=auth_user, session=session).data
