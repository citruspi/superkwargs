#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    from superkwargs import exceptions
    from superkwargs.decorator import kwarg
except ImportError:    
    import exceptions
    from decorator import kwarg