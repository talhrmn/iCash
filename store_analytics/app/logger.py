import logging

from shared.logger import setup_logger


def get_analytics_logger() -> logging.Logger:
    """Get logger for analytics application"""
    return setup_logger(
        name="iCash.Analytics",
        level="INFO",
        log_file="logs/analytics.log",
        console_output=True
    )


logger = get_analytics_logger()
