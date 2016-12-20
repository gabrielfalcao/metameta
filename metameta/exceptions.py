# -*- coding: utf-8 -*-
from metameta.functions import calculate_object_name


def repr_value_dict(data):
    return [(k, isinstance(v, basestring) and v or repr(v)) for k, v in dict(data).items()]


class InvalidMethodArgument(TypeError):
    def __init__(self, *args, **kw):
        self.__params__ = {}
        self.set_message(*args, **kw)
        super(InvalidMethodArgument, self).__init__(self.msg)

    def set_message(self, raiser_object, method_name, param_name, param_type, value, **kw):
        raiser_type = calculate_object_name(raiser_object)
        value_type = type(value)
        context = locals()
        context.pop('kw')
        context.update(**kw)
        self.__params__.update(repr_value_dict(context))

    @property
    def msg(self):
        msg = '{raiser_type}.{method_name} requires ({param_name}={param_type}). Got {value_type}: {value}'
        return msg.format(**self.__params__)


class InvalidConstructorArgument(InvalidMethodArgument):
    def __init__(self, raiser_object, param_name, param_type, value):
        method_name = '__init__'
        super(InvalidConstructorArgument, self).__init__(**locals())
