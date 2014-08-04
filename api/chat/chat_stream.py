from models.mongo import ChatMessages
from api.serializers import mChatMsgSerializer
from utils.validation import validate_mLimit


def get_chat_stream(auth_user, session, **kwargs):
    chat = kwargs['chat']
    limit_arg = kwargs['limit']
    limit, top = validate_mLimit(limit_arg)
    cms = ChatMessages.objects.filter(chat_id=chat, user_id=auth_user.id).skip(top)
    if limit:
        cms = cms.limit(limit)
    data = mChatMsgSerializer(cms, auth_user).get_data()
    return data
