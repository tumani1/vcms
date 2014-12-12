# coding:utf-8
from models.mongo import ChatMessages
from models.chats import Chats
from utils import need_authorization
from utils.exceptions import RequestErrorException


@need_authorization
def chat_send(auth_user, chat_name, session, **kwargs):
    text = kwargs['query_params'].get('text', '').strip()
    chat = session.query(Chats).filter_by(Chats.name == chat_name).first()
    if not text:
        raise RequestErrorException
    ChatMessages.objects.create(text=text, user_id=auth_user.id, chat_id=chat.id)
