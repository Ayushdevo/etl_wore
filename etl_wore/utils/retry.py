"""
Retry decorator with exponential backoff.
"""
import time
import functools
from ..logger import setup_logger

logger = setup_logger("etl_wore.utils.retry")

def retry(max_attempts: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"Max retry attempts ({max_attempts}) reached for {func.__name__}. Error: {e}")
                        raise
                    logger.warning(f"Attempt {attempt} failed for {func.__name__}: {e}. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= backoff_factor
                    attempt += 1
        return wrapper
    return decorator
