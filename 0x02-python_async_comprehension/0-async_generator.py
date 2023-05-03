#!/usr/bin/env python3
"""
0-async_generator
"""
import asyncio
from typing import Generator
import random


async def async_generator() -> Generator[float, None, None]:
    """loops 10 times and yields a float for each iteration
    after waiting for 1 sec"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
