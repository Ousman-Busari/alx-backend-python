#!/usr/bin/env python3
"""
4-tasks
"""
import asyncio


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> list:
    """runs wait_random 'n' times"""
    res = await asyncio.gather(*[task_wait_random(max_delay)
                                 for i in range(n)])
    return res
