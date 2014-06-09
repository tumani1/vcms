# coding: utf-8

from collections import OrderedDict

__all__ = ['DefaultSerializer']


class DefaultSerializer(object):

    """
        Пример заполнения массива __read_keys

        __read_keys = {
            'id': '',
            'firstname': '',
            'lastname': '',
            'user': '',
            'relation': '',
        }
    """

    __read_fields = {}
    _dict_class = OrderedDict

    def __init__(self, instance=None, user=None,
                 context=None, many=None, **kwargs):

        self.instance = instance
        self.many = many

        self.user = user
        self.is_auth = True if not user is None else False

        self.context = context or {}
        self.fields = self.__read_fields

        self._data = None
        self._errors = None

        if many and instance is not None and not hasattr(instance, '__iter__'):
            raise ValueError('instance should be a queryset or other iterable with many=True')


    @property
    def data(self):
        if self._data is None:
            obj = self.instance

            if self.many or hasattr(obj, '__iter__'):
                self._data = [self.to_native(item) for item in obj]
            else:
                self._data = self.to_native(obj)

        return self._data


    def to_native(self, obj):
        result = self._dict_class()

        for key,value in self.fields.items():
            method = getattr(self, 'get_{0}'.format(key), None)

            if callable(method):
                result[key] = method(obj)

        return result
