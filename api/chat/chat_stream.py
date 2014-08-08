from models.mongo import ChatMessages
from api.serializers import mChatMsgSerializer
from utils.validation import validate_mLimit, validate_int


def get_chat_stream(id, **kwargs):
    chat_id = validate_int(id)
    auth_user = kwargs.get('auth_user')
    limit_arg = kwargs['query']['limit']

    limit, top = validate_mLimit(limit_arg)
    cms = ChatMessages.objects.filter(chat_id=chat_id, user_id=auth_user.id).skip(top)

    if limit:
        cms = cms.limit(limit)

    return mChatMsgSerializer(cms, auth_user).get_data()
