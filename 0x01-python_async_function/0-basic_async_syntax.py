#!/usr/bin/env python3
"""
0-basic_async_syntax
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Generate a random number between 0 and max_delay,
    and delay for the number of sec before returning the
    generated number"""
    n = random.random() * max_delay
    await asyncio.sleep(n)
    return n
