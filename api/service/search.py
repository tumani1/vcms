# coding: utf-8

from Queue import Queue
from threading import Thread

from models import Persons, Topics, Media, MediaUnits, Content

from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimit, validate_string

__all__ = ['get_search_list']


def gq(model, *args, **kwargs):
    return model.get_search_by_text(**kwargs).all()

def get_search_list(auth_user, session, **kwargs):
    # Params
    params = {
        'limit': None,
        'text': None,
        'session': session,
    }

    query = kwargs['query_params']

    if 'text' in query:
        params['text'] = validate_string(query['text'])

    if 'limit' in query:
        # limit = query.get('limit', '')
        # limit, top = validate_mLimit(limit)
        params['limit'] = 10

    text = params['text']
    if text is None:
        raise RequestErrorException(u'Empty text field')

    # workers = []
    # queue = Queue()
    # mds = [Persons, Topics, Media, MediaUnits]
    #
    # for md in mds:
    #     workers.append(Thread(target=lambda q, arg, kw: q.put(gq(*arg, **kw)), args=(queue, md,), kwargs=params))
    #     workers[-1].start()
    #
    # for w in workers:
    #     w.join()
    #
    result = []
    append = result.append
    # while not queue.empty():
    #     print "Result: %s" % queue.get()

    r = {}
    con = Content.get_search_by_text(**params).all()
    for i in con:
        if not i.obj_type in r:
            r[i.obj_type] = []

        r[i.obj_type].append(i.obj_id)


    def convert_result_search(type_obj, obj):
        return {
            'type': type_obj,
            'obj': obj.__dict__,
        }

    obj_search = Persons.get_search_by_text(list_ids=r.get('', []), **params)
    for item in obj_search:
        append(convert_result_search('person', item))

    obj_search = Topics.get_search_by_text(list_ids=r.get('', []), **params)
    for item in obj_search:
        append(convert_result_search('topic', item))

    obj_search = Media.get_search_by_text(list_ids=r.get('', []), **params)
    for item in obj_search:
        append(convert_result_search('media', item))

    obj_search = MediaUnits.get_search_by_text(list_ids=r.get('', []), **params)
    for item in obj_search:
        append(convert_result_search('mediaunit', item))

    return result
