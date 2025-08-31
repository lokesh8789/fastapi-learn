import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
    encoding="utf-8",
)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or __name__)
