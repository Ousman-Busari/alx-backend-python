#!/usr/bin/env python3
"""
4-tasks
"""
import asyncio


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> list[float]:
    """runs task_wait_random n times"""
    all_tasks = [task_wait_random(max_delay) for i in range(n)]
    sorted_tasks = [await task for task in asyncio.as_completed(all_tasks)]
    return sorted_tasks
