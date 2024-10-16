import functools
from traceback import format_exc
from loguru import logger
from core.utils.helpers import sleeping
from settings import MAX_RETRIES, ACCEPTABLE_L1_GWEI
from core.clients.evm_client import EvmClient


def retry_execution(func):
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


def check_gas(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        eth_client = EvmClient()

        while True:
            try:
                gas = round(eth_client.get_gas_price() / 10**9, 2)
                if gas <= ACCEPTABLE_L1_GWEI:
                    break
                sleeping(1)
            except Exception:
                sleeping(1)

        res = func(*args, **kwargs)
        return res

    return wrapper