from models.mongo import ChatMessages
from utils import need_authorization


@need_authorization
def chat_send(auth_user, session, **kwargs):
    chat = kwargs['chat']
    text = kwargs['text']
    ChatMessages.objects.create(text=text, user_id=auth_user.id, chat_id=chat)
