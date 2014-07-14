# coding: utf-8

from collections import OrderedDict
import time
import datetime

__all__ = ['DefaultSerializer']


class DefaultSerializer(object):

    """
        Пример заполнения массива __read_keys

        __read_fields = {
            'id': '',
            'firstname': '',
            'lastname': '',
            'user': '',
            'relation': '',
        }
    """

    _dict_class = OrderedDict

    def __init__(self, instance=None, user=None,
                 context=None, session=None, **kwargs):

        self.instance = instance

        self.user = user
        self.is_auth = True if not user is None else False

        self.fields = getattr(self, '_{0}__read_fields'.format(self.__class__.__name__))
        self.context = context or {}

        self._data = None
        self._errors = None

        self.session = session

        if instance is None:
            raise ValueError('instance should be a queryset or other iterable with many=True')

    @classmethod
    @property
    def schema(cls):
        return cls.__read_fields

    @property
    def data(self):
        if self._data is None:
            obj = self.instance

            if isinstance(obj, list):
                self._data = [self.to_native(item) for item in obj]
            else:
                self._data = self.to_native(obj)

        return self._data

    def to_native(self, obj):
        result = self._dict_class()

        for key, value in self.fields.items():

            method = getattr(self, 'transform_{0}'.format(key), None) or getattr(obj, key)

            if callable(method):
                result[key] = method(obj)
            else:
                result[key] = method

        return result


def sanitize_datetime(datadict):

    answer = {}
    for key, value in datadict.items():

        if type(value) is datetime.datetime:
            answer[key] = time.mktime(value.timetuple())
        elif type(value) is dict:
            answer[key] = sanitize_datetime(value)
        else:
            answer[key] = value

    return answer
        
        
def serialize(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        assert type(result) is dict
        return sanitize_datetime(result)
    return wrapper