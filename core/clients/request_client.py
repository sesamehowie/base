import json
import requests
import pyuseragents
from typing import Self
from loguru import logger
from core.utils.exceptions import RequestFailedException


class RequestClient:
    def __init__(self, user_agent: str = None, proxy: str = None) -> Self:

        if user_agent is None:
            self.user_agent = pyuseragents.random()
        else:
            self.user_agent = user_agent

        self.proxy = proxy
        self._session = requests.Session()

    @staticmethod
    def is_successful_request(response: requests.Response):
        return True if response.status_code == 200 else False

    @staticmethod
    def get_response_obj(response: requests.Response):
        try:
            data = response.json()
        except requests.JSONDecodeError:
            logger.warning("Failed to fetch raw JSON, trying to get text info...")
            if response.text.startswith("{"):
                data = json.loads(response.text)
        finally:
            return data

    def handle_request(self, response: requests.Response) -> dict:
        if self.is_successful_request(response=response):
            return self.get_response_obj(response=response)
        raise RequestFailedException(
            f"Request is not successful, status code: {response.status_code}, text: {response.text}"
        )

    def session_get(
        self,
        url: str,
        headers: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ):
        with self._session.get(
            url=url,
            headers={"User-Agent": self.user_agent} if headers is None else headers,
            data=data,
            params=params,
            json=json,
            proxies=(
                {"http": self.proxy, "https": self.proxy}
                if self.proxy is not None
                else None
            ),
            timeout=timeout,
        ) as response:
            return self.handle_request(response)

    def session_post(
        self,
        url: str,
        headers: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ):
        with self._session.post(
            url=url,
            headers={"User-Agent": self.user_agent} if headers is None else headers,
            data=data,
            params=params,
            json=json,
            proxies=(
                {"http": self.proxy, "https": self.proxy}
                if self.proxy is not None
                else None
            ),
            timeout=timeout,
        ) as response:
            return self.handle_request(response)

    def request_get(
        self,
        url: str,
        headers: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ):
        response = requests.get(
            url=url,
            headers={"User-Agent": self.user_agent} if headers is None else headers,
            data=data,
            params=params,
            json=json,
            proxies=(
                {"http": self.proxy, "https": self.proxy}
                if self.proxy is not None
                else None
            ),
            timeout=timeout,
        )

        return self.handle_request(response)

    def request_post(
        self,
        url: str,
        headers: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ):
        response = requests.post(
            url=url,
            headers={"User-Agent": self.user_agent} if headers is None else headers,
            data=data,
            params=params,
            json=json,
            proxies=(
                {"http": self.proxy, "https": self.proxy}
                if self.proxy is not None
                else None
            ),
            timeout=timeout,
        )

        return self.handle_request(response)
