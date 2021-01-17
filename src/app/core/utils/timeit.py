from collections import Callable
from functools import wraps
from time import perf_counter_ns


SCALE_FROM_NANO_TO_MICRO = 1000
SCALE_FROM_NANO_TO_MILLI = 1000 * 1000


def async_timeit(coroutine: Callable):
    @wraps(coroutine)
    async def wrapper(*args, **kwargs):
        start: float = perf_counter_ns()
        result = await coroutine(*args, **kwargs)
        delta: float = (perf_counter_ns() - start) / SCALE_FROM_NANO_TO_MILLI
        print(f"\nElapsed time: {format(delta, '4f')} ms")
        return result

    return wrapper
