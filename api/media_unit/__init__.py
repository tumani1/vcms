from mediaunits_list import get as get_list
from mediaunits_info import get as get_info
from mediaunits_prev import get as get_prev
from mediaunits_next import get as get_next
from mediaunits_media import get as get_media

routing = (
    ('^list$', {'get': get_list}),
    ('^(?P<id>\d+)/info$', {'get': get_info}),
    ('^(?P<id>\d+)/prev$', {'get': get_prev}),
    ('^(?P<id>\d+)/next$', {'get': get_next}),
    ('^(?P<id>\d+)/media$', {'get': get_media}),
)

