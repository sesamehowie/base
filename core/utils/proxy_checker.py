import requests
import pyuseragents
from loguru import logger
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout


def is_proxy_working(url: str, proxy: str) -> bool:
    logger.debug(f"Checking proxy {proxy}...")

    successful_statuses = (200, 201, 429, 500)

    user_agent = pyuseragents.random()

    try:

        headers = {"User-Agent": user_agent}
        resp = requests.get(
            url=url,
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            headers=headers,
            timeout=120,
        )

        if resp.status_code in successful_statuses:
            return True

    except (ProxyError, ConnectTimeout, ReadTimeout):
        return False


def rule_out_faulty_proxies(proxy_list: list | tuple) -> list | tuple:
    final_list = []

    for proxy in proxy_list:

        if is_proxy_working("https://google.com", proxy):
            final_list.append(proxy)

    return final_list
