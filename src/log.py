import logging
import sys
from pathlib import Path

import pygame

from cfg import std_cfg


def setup_logger() -> None:
    """Initialize the logger for the game."""
    if Path(std_cfg.LOG_FILE).exists and not std_cfg.DEBUG_MODE:
        Path(std_cfg.LOG_FILE).unlink()
    # Create handlers
    handlers = [logging.FileHandler(std_cfg.LOG_FILE)]
    if std_cfg.LOG_TO_CONSOLE:
        handlers.append(logging.StreamHandler())

    # Basic config
    logging.basicConfig(
        level=std_cfg.LOG_LEVEL, format=std_cfg.LOG_FORMAT, datefmt=std_cfg.LOG_DATE_FORMAT, handlers=handlers
    )

    logger = logging.getLogger(__name__)
    logger.info("Logger initialized")


def log_write(message: str, level: int = logging.info) -> None:
    """Log a message with the specified level."""
    logger = logging.getLogger(__name__)
    if level <= logging.DEBUG:
        logger.debug(message)
    elif level <= logging.INFO:
        logger.info(message)
    elif level <= logging.WARNING:
        logger.warning(message)
    elif level <= logging.ERROR:
        logger.error(message)
    elif level <= logging.CRITICAL:
        logger.critical(message)
        logger.critical("Critical error detected, exiting game")
        pygame.quit()
        sys.exit(1)
    else:
        message = f"Invalid log level: {level}. Message: {message}"
        logger.error(message)
