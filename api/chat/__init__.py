from chat_info import get_chat_info
from chat_stat import get_chat_stat
from chat_stream import get_chat_stream
from chat_send import chat_send


routing = {
    'info': {
        'get': get_chat_info},
    'stat': {
        'get': get_chat_stat},
    'stream': {
        'get': get_chat_stream},
    'send': {
        'put': chat_send}
}