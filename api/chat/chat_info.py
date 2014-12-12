# coding: utf-8
from api.serializers import mChatSerializer
from models.chats import Chats


def get_chat_info(chat_name, session, **kwargs):
    c = session.query(Chats).filter(Chats.name == chat_name).first()
    data = mChatSerializer(c).get_data()
    return data
