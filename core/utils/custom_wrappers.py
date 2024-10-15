import functools
from traceback import format_exc
from loguru import logger
from core.utils.helpers import sleeping
from settings import MAX_RETRIES


def exception_handler_with_retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(MAX_RETRIES):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                logger.warning(
                    f"{func.__name__} - Traceback - {format_exc()}, exception: {repr(e)}"
                )
                sleeping(mode=1)
        else:
            return None

    return wrapper
