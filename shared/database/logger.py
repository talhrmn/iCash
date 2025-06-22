import logging

from shared.logger import setup_logger


def get_database_logger() -> logging.Logger:
    """Get logger for database operations"""
    return setup_logger(
        name="iCash.Database",
        level="INFO",
        log_file="logs/database.log",
        console_output=True
    )


logger = get_database_logger()
