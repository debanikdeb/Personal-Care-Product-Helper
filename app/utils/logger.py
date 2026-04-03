# app/core/logger.py
import logging
import os
from threading import Lock

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_logger_lock = Lock()
_global_logger = None


def get_logger(name: str = "personal-care-chatbot") -> logging.Logger:
    global _global_logger
    with _logger_lock:
        if _global_logger is None:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            # Clear any existing handlers (prevents duplicates in reloads)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # File handlers (same as before)
            file_handlers = {
                "info": logging.INFO,
                "error": logging.ERROR,
                "debug": logging.DEBUG,
                "warning": logging.WARNING,
                "critical": logging.CRITICAL,
            }

            for level_name, level in file_handlers.items():
                handler = logging.FileHandler(
                    os.path.join(LOG_DIR, f"{name}_{level_name}.log"), encoding="utf-8"
                )
                handler.setLevel(level)
                handler.setFormatter(formatter)
                logger.addHandler(handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            _global_logger = logger
        return _global_logger


logger = get_logger()
