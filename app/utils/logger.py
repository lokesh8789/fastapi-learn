import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)-5s %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
    encoding="utf-8",
)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or __name__)
