from api.serializers import mChatSerializer
from models.chats import Chats
from utils.validation import validate_int


def get_chat_info(id, auth_user, session, **kwargs):
    query = kwargs['query']
    chat = validate_int(id)

    c = session.query(Chats).get(chat)
    data = mChatSerializer(c).get_data()

    return data
