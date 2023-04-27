#!/usr/bin/env python3
"""
safely_get_value
"""
from typing import Any, Mapping, TypeVar, Union
T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """Safely get the value of a key in a dict"""
    if key in dct:
        return dct[key]
    else:
        return default
