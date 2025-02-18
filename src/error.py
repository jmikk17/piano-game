import sys
import pygame
import logging
from cfg import std_cfg

def setup_logger():
    # Create handlers
    handlers = [logging.FileHandler(std_cfg.LOG_FILE)]
    if std_cfg.LOG_TO_CONSOLE:
        handlers.append(logging.StreamHandler())

    # Basic config
    logging.basicConfig(
        level=std_cfg.LOG_LEVEL,
        format=std_cfg.LOG_FORMAT,
        datefmt=std_cfg.LOG_DATE_FORMAT,
        handlers=handlers
    )

    logging.info("Logger initialized")

# Error handling class - should be extended to non fatal error cases
def handle_error(message, error_type="fatal"):
    if error_type == "fatal":
        logging.error(f"{error_type}: {message}")
        pygame.quit()
        print(f"\nFatal error: {message}")
        print("The game will now exit.")
    elif error_type == "not_fatal":
        logging.error(f"{error_type}: {message}")


    
    sys.exit(1)