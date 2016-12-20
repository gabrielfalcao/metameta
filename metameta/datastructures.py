# -*- coding: utf-8 -*-
import re
from collections import OrderedDict
from metameta.exceptions import InvalidMethodArgument
# from metameta.exceptions import InvalidConstructorArgument


def is_valid_python_name(string):
    return re.match(r'^[a-zA-Z_][\w_]*$', string) is not None


def calculate_object_name(item, module=True):
    if not isinstance(item, type):
        return calculate_object_name(type(item))

    return br'.'.join(filter(is_valid_python_name, (module and item.__module__, item.__name__)))


def typeof(item):
    if isinstance(item, type):
        item_type = item
    else:
        item_type = type(item)

    return repr(item_type)


class DynamicKeyDict(dict):
    # TODO: test that __formatkey__() is called by __init__ for both
    # *args and **kw

    def __init__(self, data=None, **kw):
        super(DynamicKeyDict, self).__init__()
        self.__setup__()
        data = data or {}

        if isinstance(data, (list, OrderedDict)):
            self.update(data)

        elif isinstance(data, dict):
            kw.update(data)

        for key in self.__sortkeys__(kw.keys()):
            self[key] = kw[key]

    def __setup__(self):
        pass

    def __sortkeys__(self, keys):
        return sorted(keys)

    def __processkey__(self, key):
        key = self.__validatekey__(key)
        key = self.__formatkey__(key)
        return key

    def __processvalue__(self, key, value):
        return value

    def __validatekey__(self, key):
        if not isinstance(key, basestring):
            raise InvalidMethodArgument(self, '__validatekey__', 'key', basestring, key)

        return key

    def __setitem__(self, key, value):
        key = self.__processkey__(key)
        value = self.__processvalue__(key, value)
        return super(DynamicKeyDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        key = self.__processkey__(key)
        return super(DynamicKeyDict, self).__getitem__(key)

    def __formatkey__(self, key):
        return key


class CaseInsensitiveDict(DynamicKeyDict):
    def __formatkey__(self, key):
        return key.lower()


class ObjectDict(DynamicKeyDict):
    def __formatkey__(self, key):
        return br'${}'.format(key)


def inspect_members(obj):
    return filter(lambda _: not _.startswith('_'), dir(obj))


def is_builtin_serializable(value):
    return isinstance(value, (list, tuple, dict, basestring, long, int, complex, float, OrderedDict, ObjectDict, CaseInsensitiveDict, DynamicKeyDict))


def sentinel(x):
    return x


def extract_from_opaque(obj, key_transform=sentinel, value_transform=sentinel):
    if not callable(key_transform):
        raise TypeError('extract_from_opaque() key_transform must be callable')

    keys = inspect_members(obj)
    values = map(lambda k: getattr(obj, k, None), keys)

    return ((key_transform(key), value_transform(value)) for key, value in zip(keys, values) if is_builtin_serializable(value))
