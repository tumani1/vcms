from models.mongo import ChatMessages
from api.serializers import mChatMsgSerializer
from utils.validation import validate_mLimit, validate_int


def get_chat_stream(id, **kwargs):
    chat_id = validate_int(id)
    session = kwargs.get('session')
    limit = kwargs['query']['limit']

    limit, top = validate_mLimit(limit)
    cms = ChatMessages.objects.filter(chat_id=chat_id).skip(top)

    if limit:
        cms = cms.limit(limit)

    return mChatMsgSerializer(cms, session).get_data()
