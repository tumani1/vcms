from api.serializers import mChatSerializer
from models.chats import Chats
from utils.validation import validate_int


def get_chat_info(id, **kwargs):
    query = kwargs['query']
    chat_id = validate_int(id)
    session = kwargs.get('session')

    c = session.query(Chats).get(chat_id)
    data = mChatSerializer(c).get_data()

    return data
