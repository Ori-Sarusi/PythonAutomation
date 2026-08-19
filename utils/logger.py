import logging
import sys
import os

def get_logger(name: str = "TestAutomation") -> logging.Logger:
    """Creates a configured logger that integrates cleanly with pytest log capturing."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
