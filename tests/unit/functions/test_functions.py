# -*- coding: utf-8 -*-

from metameta.datastructures import ObjectDict
from metameta.functions import is_valid_python_name
from metameta.functions import calculate_object_name
from metameta.functions import typeof


def test_is_valid_python_name():
    is_valid_python_name('Good_ch0ic3').should.be.true
    is_valid_python_name('@foobar').should.be.false
    is_valid_python_name('-asd').should.be.false


def test_calculate_object_name():
    class_type = ObjectDict
    class_instance = ObjectDict()

    calculate_object_name(class_type).should.equal('metameta.datastructures.ObjectDict')
    calculate_object_name(class_instance).should.equal('metameta.datastructures.ObjectDict')


def test_typeof():
    typeof(ObjectDict({'foo': 'bar'})).should.equal("<class 'metameta.datastructures.ObjectDict'>")
