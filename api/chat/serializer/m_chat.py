# coding=utf-8
from models.chats import Chats


class mChatSerializer(object):

    def __init__(self, chat):
        if chat is None:
            raise TypeError("attr must not be None")

        if not isinstance(chat, Chats):
            raise TypeError("attr is not Chats instance")

        self.chat = chat

    def get_data(self):
        return dict(id=self.chat.id, description=self.chat.description)