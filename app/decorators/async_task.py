import asyncio
from functools import wraps
import inspect
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar
from app.configs.db_config import async_session

P = ParamSpec("P")
R = TypeVar("R")

def run_async(func: Callable[P, R] | Callable[P, Awaitable[R]]) -> Callable[P, "asyncio.Task[R]"]:
    is_async = inspect.iscoroutinefunction(func)
    sig = inspect.signature(func)
    expects_db = "db" in sig.parameters
    if expects_db and not is_async:
        raise RuntimeError(
            f"@scheduled error: '{func.__name__}' expects DB but is not async."
        )
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> "asyncio.Task[R]":
        async def run_job() -> R:
            if expects_db:
                async with async_session() as db:
                    if is_async:
                        return await func(db, *args, **kwargs)
                    else:
                        raise RuntimeError(
                            f"@scheduled function '{func.__name__}' expects DB but is not async."
                        )
            else:
                if is_async:
                    return await func(*args, **kwargs)
                else:
                    return await asyncio.to_thread(func, *args, **kwargs)
        print("Running Job")
        return asyncio.create_task(run_job())
    return wrapper
    