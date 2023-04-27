#!/usr/bin/env python3
"""
safe_first_element
"""
from typing import Any, List, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """returns the firs element of lst, if lst is true, else
    returns None
    """
    if lst:
        return lst[0]
    else:
        return None
