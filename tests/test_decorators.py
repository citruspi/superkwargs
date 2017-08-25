#!/usr/bin/env python
# -*- coding: utf8 -*-

from superkwargs import superkwarg, kwarg, exceptions
from nose.tools import raises


def test_required_kwarg():
    @kwarg('name', required=True)
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.MissingRequiredKwargException)
def test_missing_required_kwarg():
    @kwarg('name', required=True)
    def foobar(**kwargs):
        pass

    foobar()


@raises(exceptions.PositionalArgsIncludedException)
def test_positional_arguments_included():
    @kwarg('name')
    def foobar(**kwargs):
        pass

    foobar(None)


def test_valid_kwarg_value():
    @kwarg('name', choices=['bender', 'zoidberg'])
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.InvalidKwargValueException)
def test_invalid_kwarg_value():
    @kwarg('name', choices=['bender', 'hermes'])
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


def test_kwarg_value_validation_success():
    @kwarg('name', validation_test=lambda name: name=='zoidberg')
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.KwargValueValidationException)
def test_kwarg_value_validation_failure():
    @kwarg('name', validation_test=lambda name: name=='robot devil')
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


def test_kwarg_value_type():
    @kwarg('name', type_=str)
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.WrongKwargValueTypeException)
def test_wrong_kwarg_value_type():
    @kwarg('name', type_=str)
    def foobar(**kwargs):
        pass

    foobar(name={})


def test_inject_kwargs():
    @kwarg('name')
    @superkwarg(inject=True)  
    def foobar(**kwargs):
        return name

    assert foobar(name='zoidberg') == 'zoidberg'


@raises(NameError)
def test_dont_inject_kwargs():
    @kwarg('name')
    def foobar(**kwargs):
        return name

    foobar(name='zoidberg')