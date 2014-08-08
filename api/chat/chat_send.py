from models.mongo import ChatMessages
from utils import need_authorization
from utils.validation import validate_int

@need_authorization
def chat_send(id, **kwargs):
    chat_id = validate_int(id)
    auth_user = kwargs.get('auth_user')
    text = kwargs['query']['text']
    ChatMessages.objects.create(text=text, user_id=auth_user.id, chat_id=chat_id)
