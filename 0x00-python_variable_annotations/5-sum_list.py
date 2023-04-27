#!/usr/bin/env python3
"""
sum_list
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Returns the sum of a list of float"""
    sum: float = 0.0
    for i in input_list:
        sum += i
    return sum
