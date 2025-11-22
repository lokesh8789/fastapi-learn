from __future__ import annotations

import asyncio
import inspect
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from apscheduler.triggers.cron import CronTrigger  # type: ignore
from apscheduler.triggers.date import DateTrigger  # type: ignore
from apscheduler.triggers.interval import IntervalTrigger  # type: ignore

from app.configs.db_config import async_session

# Global scheduler instance
scheduler = AsyncIOScheduler()


def scheduled(
    *,
    cron: str | None = None,
    fixedRate: int | None = None,  # milliseconds like Spring Boot
    initialDelay: int | None = None,  # milliseconds before first run
    zone: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Spring Boot-style @Scheduled decorator for FastAPI.

    Parameters:
    - cron: cron expression ("*/10 * * * * *" for every 10 seconds)
    - fixedRate: run every N milliseconds from start time
    - initialDelay: wait before first run (ms)
    - zone: timezone string (e.g., "Asia/Kolkata")
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        is_async = inspect.iscoroutinefunction(func)
        sig = inspect.signature(func)
        expects_db = "db" in sig.parameters
        if expects_db and not is_async:
            raise RuntimeError(
                f"@scheduled error: '{func.__name__}' expects DB but is not async."
            )

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async def run_job():
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
            asyncio.create_task(run_job())
            return

        tz = ZoneInfo(zone) if zone else None

        # Compute next run for initialDelay only for interval/fixedDelay
        start_at: datetime | None = None
        if initialDelay is not None:
            start_at = datetime.now(tz) + timedelta(milliseconds=initialDelay)

        if cron:
            # For cron, APScheduler automatically calculates next run if next_run_time=None
            scheduler.add_job(
                wrapper,
                build_cron_trigger(cron, tz),
            )
        elif fixedRate is not None:
            if start_at is not None:
                scheduler.add_job(
                    wrapper,
                    IntervalTrigger(seconds=fixedRate / 1000.0, timezone=tz),
                    next_run_time=start_at,
                )
            else:
                scheduler.add_job(
                    wrapper,
                    IntervalTrigger(seconds=fixedRate / 1000.0, timezone=tz),
                )
        else:
            raise ValueError("One of cron or fixedRate must be set")

        return wrapper

    return decorator


def build_cron_trigger(cron: str, tz: ZoneInfo | None = None) -> CronTrigger:
    """
    Build an APScheduler CronTrigger from a Spring Boot-style cron string.
    Supports 6-field cron (seconds included) or 5-field cron (no seconds).
    """
    fields = cron.strip().split()
    if len(fields) == 6:
        second, minute, hour, day, month, day_of_week = fields
        return CronTrigger(
            second=second,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            timezone=tz,
        )
    elif len(fields) == 5:
        minute, hour, day, month, day_of_week = fields
        return CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            timezone=tz,
        )
    else:
        raise ValueError(f"Invalid cron expression, got {len(fields)} fields: {cron}")
