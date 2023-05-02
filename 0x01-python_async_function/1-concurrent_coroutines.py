#!/usr/bin/env python3
"""
1-concurrent_coroutines
"""
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    """runs wait_random n times"""
    all_tasks = [asyncio.create_task(wait_random(max_delay)) for i in range(n)]
    sorted_tasks = [await task for task in asyncio.as_completed(all_tasks)]
    return sorted_tasks
