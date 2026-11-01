"""
Retry decorator with exponential backoff.
"""
import math
import time
from threading import TIMEOUT_MAX
import functools
from ..logger import setup_logger

logger = setup_logger("etl_wore.utils.retry")

def retry(max_attempts: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0, exceptions=(Exception,)):
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    for name, value in (("initial_delay", initial_delay), ("backoff_factor", backoff_factor)):
        try:
            valid = isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError(f"{name} must be a finite number")
    if not math.isfinite(initial_delay) or initial_delay < 0:
        raise ValueError("initial_delay must be finite and nonnegative")
    if not math.isfinite(backoff_factor) or backoff_factor <= 0:
        raise ValueError("backoff_factor must be finite and positive")

    filters = exceptions if isinstance(exceptions, tuple) else (exceptions,)
    if any(not isinstance(kind, type) or not issubclass(kind, BaseException) for kind in filters):
        raise ValueError('exceptions must be an exception class or a tuple of exception classes')

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = min(initial_delay, TIMEOUT_MAX)
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
                    delay = min(delay * backoff_factor, TIMEOUT_MAX)
                    attempt += 1
        return wrapper
    return decorator
