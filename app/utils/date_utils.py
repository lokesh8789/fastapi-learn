from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# India Standard Time (IST)
IST = ZoneInfo("Asia/Kolkata")


class DateUtil:
    @staticmethod
    def now_ist() -> datetime:
        """Return current datetime in IST."""
        return datetime.now(IST)

    @staticmethod
    def today_ist() -> datetime:
        """Return today's date at 00:00:00 IST."""
        return datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def format(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime object into a string in IST."""
        return dt.astimezone(IST).strftime(fmt)

    @staticmethod
    def parse(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """Parse string into datetime in IST."""
        return datetime.strptime(date_str, fmt).replace(tzinfo=IST)

    @staticmethod
    def add_minutes(minutes: int) -> datetime:
        """Return IST datetime with given minutes added."""
        return datetime.now(IST) + timedelta(minutes=minutes)

    @staticmethod
    def add_days(days: int) -> datetime:
        """Return IST datetime with given days added."""
        return datetime.now(IST) + timedelta(days=days)
