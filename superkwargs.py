#!/usr/bin/env python
# -*- coding: utf8 -*-


class SuperkwargException(Exception):
    pass


class MissingRequiredKwargException(SuperkwargException):
    pass


class InvalidKwargValueException(SuperkwargException):
    pass


class KwargValueValidationException(SuperkwargException):
    pass


def kwarg(name, required=False, default=None, evaluate_default=False,
          choices=None, validation_test=None):
    def decorator(function):
        def superkwarg(*args, **kwargs):
            if required and name not in kwargs:
                raise MissingRequiredKwargException(
                    'Keyword argument \'{arg}\' required to invoke \'{func}\''.format(
                    arg=name, func=function.__name__))

            if name not in kwargs:
                if evaluate_default:
                    kwargs[name] = default(kwargs)
                else:
                    kwargs[name] = default

            if (choices is not None) and (kwargs[name] not in choices):
                raise InvalidKwargValueException(
                    'Keyword argument \'{arg}\' value \'{value}\' not in available choices {choices}'.format(
                        arg=name,
                        value=kwargs[name],
                        choices=choices
                    )
                )

            if validation_test is not None and not validation_test(kwargs[name]):
                raise KwargValueValidationException(
                    'Keyword argument \'{arg}\' value \'{value}\' failed validation test'.format(
                        arg=name,
                        value=kwargs[name]
                    )
                )

            return function(*args, **kwargs)
        return superkwarg
    return decorator