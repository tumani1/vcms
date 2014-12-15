# coding: utf-8

from Queue import Queue
from threading import Thread

from models import Persons, Topics, Media, MediaUnits, Content
from utils.constants import OBJECT_TYPE_PERSON, OBJECT_TYPE_TOPIC, OBJECT_TYPE_MEDIA_UNIT, OBJECT_TYPE_MEDIA

from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimit, validate_string

__all__ = ['get_search_list']


MODELS_TO_PARAMS = {
    Persons: (OBJECT_TYPE_PERSON, 'person',),
    Topics: (OBJECT_TYPE_TOPIC, 'topic',),
    Media: (OBJECT_TYPE_MEDIA, 'media',),
    MediaUnits: (OBJECT_TYPE_MEDIA_UNIT, 'mediaunit',),
}

convert_result_search = lambda type_obj, obj: {'type': type_obj, 'obj': obj.as_dict}


def gq(model, *args, **kwargs):
    type_row = MODELS_TO_PARAMS[model]
    return [convert_result_search(type_row[1], item) for item in model.get_search_by_text(**kwargs)]


def get_search_list(auth_user, session, **kwargs):
    # Params
    params = {
        'limit': None,
        'text': None,
        'session': session,
        'list_ids': [],
    }

    query = kwargs['query_params']

    if 'text' in query:
        params['text'] = validate_string(query['text'])

    if 'limit' in query:
        params['limit'] = validate_mLimit(query['limit'])

    if params['text'] is None:
        raise RequestErrorException(u'Empty text field')

    result = []
    append = result.append

    content_ids = {}
    con = Content.get_search_by_text(**params)
    for i in con:
        if not i.obj_type.code in content_ids:
            content_ids[i.obj_type.code] = []

        content_ids[i.obj_type.code].append(i.obj_id)

    # workers = []
    # queue = Queue()
    #
    # for md in mds.keys():
    #     list_ids = content_ids.get(mds[Persons], [])
    #     if len(list_ids):
    #         params.update({'list_ids': list_ids})
    #         workers.append(Thread(target=lambda q, arg, kw: q.put(gq(*arg, **kw)), args=(queue, md,), kwargs=params))
    #         workers[-1].start()
    #
    # for w in workers:
    #     w.join()
    #
    # while not queue.empty():
    #     print "Result: %s" % queue.get()
    #     append(convert_result_search(queue.get()))

    for key, val in MODELS_TO_PARAMS.items():
        list_ids = content_ids.get(val[0], [])
        if len(list_ids):
            params.update({'list_ids': list_ids})
            temp = [convert_result_search(val[1], item) for item in key.get_search_by_text(**params)]

            if len(temp):
                result.extend(temp)

    return result
