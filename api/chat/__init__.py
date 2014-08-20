from chat_info import get_chat_info
from chat_stat import get_chat_stat
from chat_stream import get_chat_stream
from chat_send import chat_send


routing = (
    (r'^(?P<chat_id>\d+)/info$', {'get': get_chat_info}),
    (r'^(?P<chat_id>\d+)/stat$', {'get': get_chat_stat}),
    (r'^(?P<chat_id>\d+)/stream$', {'get': get_chat_stream}),
    (r'^(?P<chat_id>\d+)/send$', {'put': chat_send})
)
