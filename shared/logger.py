import logging
import sys
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',
        'INFO': '\033[32m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[35m',
        'RESET': '\033[0m'
    }

    def format(self, record):
        level = record.levelname
        if level in self.COLORS:
            record.levelname = f"{self.COLORS[level]}{level}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger(
        name: str,
        level: str = "INFO",
        log_file: Optional[str] = None,
        console_output: bool = True
) -> logging.Logger:
    logger = logging.getLogger(name)
    # Convert level string to numeric
    lvl = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(lvl)

    # If handlers already set for this logger, skip adding duplicates
    # But you might want to clear and re-add if configuration changed
    # Here, we clear to ensure fresh config:
    logger.handlers.clear()

    # Console formatter
    simple_fmt = '%(asctime)s | %(levelname)s | %(message)s'
    detailed_fmt = '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    simple_formatter = ColoredFormatter(fmt=simple_fmt, datefmt='%H:%M:%S')
    detailed_formatter = logging.Formatter(fmt=detailed_fmt, datefmt=datefmt)

    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(lvl)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file)
        # Ensure directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(lvl)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        # Optionally print where logs go
        print(f"[Logger] {name}: logging to file {log_path.resolve()}")

    # Prevent messages from propagating to root logger (avoids duplicate logs or missing logs)
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
