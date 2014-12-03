# coding: utf-8
from models.chats import Chats
from utils.exceptions import RequestErrorException


class mChatSerializer(object):

    def __init__(self, chat):
        if chat is None:
            raise RequestErrorException("attr must not be None")

        if not isinstance(chat, Chats):
            raise RequestErrorException("attr is not Chats instance")

        self.chat = chat

    def get_data(self):
        return dict(id=self.chat.id, description=self.chat.description)