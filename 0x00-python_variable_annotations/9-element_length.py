#!/usr/bin/env python3
"""
element_length
"""
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuple with each element and its index
    as the first and second elemt of each tuple"""
    return [(i, len(i)) for i in lst]
