# coding: utf-8
from models.mongo import ChatMessages
from models.chats import Chats
from api.serializers import mChatMsgSerializer
from utils.validation import validate_mLimit


def get_chat_stream(chat_name, session, **kwargs):
    chat = session.query(Chats).filter(Chats.name == chat_name).first()
    limit = kwargs['query_params'].get('limit', '')
    limit, top = validate_mLimit(limit)
    cms = ChatMessages.objects.filter(chat_id=chat.id)
    if top:
        cms = cms.skip(top)
    if limit:
        cms = cms.limit(limit)

    return mChatMsgSerializer(cms, session).get_data()
