#!/usr/bin/env python3
"""
sum_mixed_list
"""
from typing import List, Union


def sum_mixed_list(mxd_list: List[Union[int, float]]) -> float:
    """Returns the sum of a mixed list with int and float, as a gloat"""
    sum: float = 0.0
    for i in mxd_list:
        sum += i
    return sum
