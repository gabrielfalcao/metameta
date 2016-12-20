# -*- coding: utf-8 -*-
from metameta.datastructures import DynamicKeyDict
from metameta.exceptions import InvalidMethodArgument


def test_init_validate_keys():
    DynamicKeyDict.when.called_with({232: 23}).should.have.raised(
        InvalidMethodArgument,
        "DynamicKeyDict.__validatekey__ requires (key=<type 'basestring'>). Got <type 'int'>: 232",
    )
