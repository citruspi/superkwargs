#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    from superkwargs import exceptions
except ImportError:
    import exceptions

def kwarg(name, required=False, default=None, evaluate_default=False,
          choices=None, validation_test=None):
    def decorator(function):
        def superkwarg(*args, **kwargs):
            if len(args) > 0:
                raise exceptions.PositionalArgsIncludedException(
                    'Positional argument \'{arg}\' not allowed; kwargs are required'.format(
                        arg=args[0]
                    ))

            if required and name not in kwargs:
                raise exceptions.MissingRequiredKwargException(
                    'Keyword argument \'{arg}\' required to invoke \'{func}\''.format(
                        arg=name, func=function.__name__))

            if name not in kwargs:
                if evaluate_default:
                    kwargs[name] = default(kwargs)
                else:
                    kwargs[name] = default

            if (choices is not None) and (kwargs[name] not in choices):
                raise exceptions.InvalidKwargValueException(
                    'Keyword argument \'{arg}\' value \'{value}\' not in available choices {choices}'.format(
                        arg=name,
                        value=kwargs[name],
                        choices=choices
                    )
                )

            if validation_test is not None and not validation_test(kwargs[name]):
                raise exceptions.KwargValueValidationException(
                    'Keyword argument \'{arg}\' value \'{value}\' failed validation test'.format(
                        arg=name,
                        value=kwargs[name]
                    )
                )

            _blank = object()

            state = {k:function.__globals__.get(k, _blank) for k in kwargs}
            function.__globals__.update(kwargs)

            try:
                return function()
            finally:
                for k, v in state.items():
                    if v == _blank:
                        del function.__globals__[k]
                    else:
                        function.__globals__[k] = v

        return superkwarg
    return decorator