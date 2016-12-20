# -*- coding: utf-8 -*-
import re


def is_valid_python_name(string):
    if not isinstance(string, basestring):
        return False

    return re.search(r'^[a-zA-Z_][\w_]*$', string) is not None


def calculate_object_name(item, module=True):
    if not isinstance(item, type):
        return calculate_object_name(type(item), module=module)

    return br'.'.join((item.__module__, item.__name__))


def typeof(item):
    return repr(type(item))


class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


def is_number(value):
    return isinstance(value, (long, int, complex, float))


def is_string(value):
    return isinstance(value, (basestring, str, bytes, unicode))


def is_iterable(value):
    # only things that can be json-serialized
    return isinstance(value, (list, dict, tuple))


def is_container(value):
    return isinstance(value, (set, frozenset)) or is_iterable(value)


def is_serializable(value):
    return isinstance(value, (list, tuple, dict, basestring)) or is_number(value)
