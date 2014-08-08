from models.mongo import ChatMessages
from utils import need_authorization
from utils.validation import validate_int

@need_authorization
def chat_send(id, auth_user, session, **kwargs):
    chat = validate_int(id)
    text = kwargs['query']['text']
    ChatMessages.objects.create(text=text, user_id=auth_user.id, chat_id=chat)
