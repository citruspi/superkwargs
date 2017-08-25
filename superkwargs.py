#!/usr/bin/env python
# -*- coding: utf8 -*-


class SuperkwargException(Exception):
    pass


class MissingRequiredKwargException(SuperkwargException):
    pass


def kwarg(name, required=False):    
    def decorator(function):
        def superkwarg(*args, **kwargs):
            if required and name not in kwargs:
                raise MissingRequiredKwargException(
                    'Keyword argument \'{arg}\' required to invoke \'{func}\''.format(
                    arg=name, func=function.__name__))

            return function(*args, **kwargs)
        return superkwarg
    return decorator