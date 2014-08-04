from api.serializers import mChatSerializer
from models.chats import Chats


def get_chat_info(auth_user, session, **kwargs):
    query = kwargs['query']
    chat = query['chat']

    c = session.query(Chats).get(chat)
    data = mChatSerializer(c).get_data()

    return data
