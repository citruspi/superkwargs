#!/usr/bin/env python
# -*- coding: utf8 -*-

from superkwargs import superkwarg, kwarg, exceptions
from nose.tools import raises


def test_required_kwarg():
    @kwarg('name', required=True)
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.MissingRequiredKwargException)
def test_missing_required_kwarg():
    @kwarg('name', required=True)
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar()


def test_default_kwarg():
    @kwarg('name', default='zoidberg')
    @superkwarg()
    def foobar(**kwargs):
        return kwargs['name']

    assert foobar() == 'zoidberg'


def test_lambda_default_kwarg():
    @kwarg('name', default='zoidberg')
    @kwarg('message', default=lambda kw: 'hello {}'.format(kw['name']))
    @superkwarg()
    def foobar(**kwargs):
        return kwargs['message']

    assert foobar() == 'hello zoidberg'    


def test_function_default_kwarg():
    def hello_world(kw):
        return 'hello {}'.format(kw['name'])

    @kwarg('name', default='zoidberg')
    @kwarg('message', default=hello_world)
    @superkwarg()
    def foobar(**kwargs):
        return kwargs['message']

    assert foobar() == 'hello zoidberg'     


def test_callable_default_kwarg_no_invoke():
    def hello_world(kw):
        return 'hello {}'.format(kw['name'])

    @kwarg('name', default='zoidberg')
    @kwarg('message', default=hello_world, invoke_default=False)
    @superkwarg()
    def foobar(**kwargs):
        return kwargs['message']

    assert foobar() == hello_world           


@raises(exceptions.PositionalArgsIncludedException)
def test_positional_arguments_included():
    @kwarg('name')
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(None)


def test_valid_kwarg_value():
    @kwarg('name', choices=['bender', 'zoidberg'])
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.InvalidKwargValueException)
def test_invalid_kwarg_value():    
    @kwarg('name', choices=['bender', 'hermes'])
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


def test_kwarg_value_validation_success():
    @kwarg('name', validation_test=lambda name: name=='zoidberg')
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.KwargValueValidationException)
def test_kwarg_value_validation_failure():
    @kwarg('name', validation_test=lambda name: name=='robot devil')
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


    def foobar(name=None):
        if name is None:
            name == 'zoidberg'

    @kwarg('name', default='zoidberg')
    def foobar(**kwargs):
        pass

    foobar()

def test_kwarg_value_type():
    @kwarg('name', types=['str'])
    @superkwarg()
    def foobar(**kwargs):
        pass

    foobar(name='zoidberg')


@raises(exceptions.WrongKwargValueTypeException)
def test_wrong_kwarg_value_type():
    @kwarg('name', types=['str'])
    @superkwarg()
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
    @superkwarg()
    def foobar(**kwargs):
        return name

    foobar(name='zoidberg')


def test_kwargs_on_method():
    class Foobar(object):
        name = None

        @kwarg('name', required=True)
        @superkwarg()
        def __init__(self, **kwargs):
            self.name = kwargs['name']

    assert Foobar(name='zoidberg').name == 'zoidberg'


def test_inject_kwargs_on_method():
    class Foobar(object):
        name = None

        @kwarg('name', required=True)
        @superkwarg(inject=True)  
        def __init__(self, **kwargs):
            self.name = name

    assert Foobar(name='zoidberg').name == 'zoidberg'


def test_kwargs_on_class_method():
    class Foobar(object):
        multiplier = 2

        @classmethod
        @kwarg('x')
        @superkwarg()
        def multiply(cls, **kwargs):
            return cls.multiplier * kwargs['x']

    assert Foobar.multiply(x=5) == 10


def test_kwargs_on_static_method():
    class Foobar(object):
        
        @staticmethod
        @kwarg('name')
        @superkwarg()
        def foo(**kwargs):
            return kwargs['name']

    assert Foobar.foo(name='zoidberg') == 'zoidberg'
        