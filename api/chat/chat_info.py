from api.serializers import mChatSerializer
from models.chats import Chats
from utils.validation import validate_int


def get_chat_info(chat_id, **kwargs):
    query = kwargs['query_params']
    chat_id = validate_int(chat_id)
    session = kwargs.get('session')

    c = session.query(Chats).get(chat_id)
    data = mChatSerializer(c).get_data()

    return data
