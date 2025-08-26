import inspect
from functools import wraps
from typing import Callable


def log(val: str):
    def inner(func: Callable):
        if inspect.iscoroutinefunction(func):
            # Handle async functions
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                print(f"[LOG]: {val}")
                print(f"[ARGS]: {args}")
                print(f"[KWARGS]: {kwargs}")
                res = await func(*args, **kwargs)
                print(f"[RESULT]: {res}")
                return res

            return async_wrapper
        else:
            # Handle sync functions
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                print(f"[LOG]: {val}")
                print(f"[ARGS]: {args}")
                print(f"[KWARGS]: {kwargs}")
                res = func(*args, **kwargs)
                print(f"[RESULT]: {res}")
                return res

            return sync_wrapper

    return inner
