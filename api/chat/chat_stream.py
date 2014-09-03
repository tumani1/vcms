# coding: utf-8
from models.mongo import ChatMessages
from api.serializers import mChatMsgSerializer
from utils.validation import validate_mLimit, validate_int


def get_chat_stream(chat_id, **kwargs):
    chat_id = validate_int(chat_id, min_value=1)
    session = kwargs.get('session')
    limit = kwargs['query_params'].get('limit', '')
    limit, top = validate_mLimit(limit)
    cms = ChatMessages.objects.filter(chat_id=chat_id)

    if top:
        cms = cms.skip(top)

    if limit:
        cms = cms.limit(limit)

    return mChatMsgSerializer(cms, session).get_data()
