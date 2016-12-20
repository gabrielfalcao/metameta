# -*- coding: utf-8 -*-
import re
import sys
import multiprocessing
from types import NoneType
from metameta.functions import typeof

DEFAULT_PBKDF2_ITERATIONS = multiprocessing.cpu_count() ** 1000

SYMBOLS = {}


class SymbolHasher(object):
    def __call__(self, value):
        if not isinstance(value, Symbol):
            raise TypeError('SymbolHasher() needs a Symbol as argument, not {}'.format(typeof(value)))

        return self.process_hash(value)

    def process_hash(self, string):
        raise NotImplementedError


class PBKDF2Hasher(SymbolHasher):
    def __init__(self, algorithm='sha256', iterations=0):
        iterations = iterations or DEFAULT_PBKDF2_ITERATIONS


class ModuleSymbolRegistry(object):
    def __init__(self, name, parent=None):
        self.name = name
        if not isinstance(parent, (NoneType, SymbolTree)):
            raise TypeError('Module() argument parent')

    @property
    def ref(self):
        return sys.modules[self.name]

    @property
    def storage(self):
        return SymbolStorage(self)


class SymbolStorage(object):
    def __init__(self, module):
        self.module = module


default_secure_hash = PBKDF2Hasher


def parse_symbolic_string(string):
    found = re.search(r'(?P<modhash>[$]w+)', string)
    if found:
        return found.group(1)


def get_tree_for_symbolic_string(string):
    pass


class Symbol(bytes):
    def __init__(self, string, tree=None):
        tree = tree or get_tree_for_symbolic_string(string)
        self.__tree__ = tree
        self.__raw__ = string
        super(Symbol, self).__init__(self.__raw__)

    def __str__(self):
        return bytes.__str__(self)

    def __unicode__(self):
        return unicode.__str__(self)

    def __hash__(self):
        return self.__tree__.checksum(self)

    def __repr__(self):
        return '${}'.format(bytes())


class SymbolTree(object):
    def __init__(self, module_name, compute_hash=default_secure_hash):
        self.module_name = module_name
        self.compute_hash = compute_hash

    def __hash__(self):
        return self.compute_hash(self.module_name)

    def __call__(self, string):
        return Symbol(string, tree=self)


S = SymbolTree(__name__)
