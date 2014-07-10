from serializer import mChatSerializer
from models.chats import Chats


def get_chat_info(auth_user, session, **kwargs):
    chat = kwargs['chat']
    c = session.query(Chats).get(chat)
    data = mChatSerializer(c).get_data()
    return data