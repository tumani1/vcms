# coding: utf-8


def get(id, query, **kwargs):
    return {
        'id': id,
        'title': 'Parameters is {0}'.format(id)
    }