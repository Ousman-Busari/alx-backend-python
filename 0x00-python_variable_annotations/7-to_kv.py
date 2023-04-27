#!/usr/bin/env python3
"""
to_kv
"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns a tuple with the first argument as its first elements in string,
    and the square of the second argument as its second element in float
    """
    return (k, v ** 2)
