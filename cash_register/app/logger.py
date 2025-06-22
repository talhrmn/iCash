import logging

from shared.logger import setup_logger


def get_cashier_logger() -> logging.Logger:
    """Get logger for cash_register application"""
    return setup_logger(
        name="iCash.Cashier",
        level="INFO",
        log_file="logs/app_a_cashier.log",
        console_output=True
    )


logger = get_cashier_logger()
