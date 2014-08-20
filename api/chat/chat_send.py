#coding:utf-8
from models.mongo import ChatMessages
from utils import need_authorization
from utils.validation import validate_int


@need_authorization
def chat_send(chat_id, **kwargs):  # TODO: что делать при отсутствии текста или пустом тексте?
    chat_id = validate_int(chat_id, min_value=1)
    auth_user = kwargs.get('auth_user')
    text = kwargs['query'].get('text', '')
    ChatMessages.objects.create(text=text, user_id=auth_user.id, chat_id=chat_id)
