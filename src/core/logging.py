import sys
from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>",
    level="DEBUG",
    backtrace=True,
    diagnose=True,
    enqueue=True,
)

logger.add(
    LOG_DIR / "errors.log",
    rotation="10 MB",
    retention="10 days",
    level="ERROR",
    backtrace=True,
    diagnose=True,
    enqueue=True,
    compression="zip",
)

logger.add(
    LOG_DIR / "audit.log",
    rotation="5 MB",
    retention="30 days",
    level="INFO",
    filter=lambda record: "AUDIT" in record["extra"],
    enqueue=True,
)


def audit(message: str, **kwargs):
    logger.bind(AUDIT=True).info(message, **kwargs)


__all__ = ["logger", "audit"]
