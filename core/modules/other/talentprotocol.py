import json
from typing import Self
from eth_account import Account
from core.utils.w3_manager import EthManager
from web3 import Web3
from fake_useragent import UserAgent
from eth_account.messages import encode_defunct
import requests
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.custom_wrappers import exception_handler_with_retry
from core.utils.helpers import get_browser_version


class TalentProtocol:
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        proxy: str,
    ) -> Self:

        self.logger = logger
        self.private_key = private_key
        self.account_name = account_name
        self.account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network = network
        self.user_agent = UserAgent(min_version=120.0, os="windows").random
        self.proxy = proxy
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "Talent Protocol"
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.logger.debug(f"Now working: module {self.module_name}")

    @exception_handler_with_retry
    def get_nonce(self):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Getting nonce..."
        )

        url = "https://login.talentprotocol.com/auth/login_nonces"

        chrome_version = get_browser_version(self.user_agent)

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://login.talentprotocol.com/join",
            "Priority": "u=1, i",
            "Referer": "https://login.talentprotocol.com/join",
            "Sec-Ch-Ua": f'"Chromium";v="{chrome_version}", "Not;A=Brand";v="24", "Google Chrome";v="{chrome_version}"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.user_agent,
        }

        payload = {"address": self.address}

        response = requests.post(
            url=url, headers=headers, json=payload, proxies=self.default_proxies
        )

        if response.status_code == 200:
            return json.loads(response.text)["nonce"]
        else:
            raise

    def sign_message(self, nonce: str) -> str:
        message = f"Sign in with Talent Protocol\nnonce: {nonce}"

        hashable = encode_defunct(text=message)

        signature = Web3.to_hex(
            self.account.sign_message(signable_message=hashable).signature
        )

        return signature

    @exception_handler_with_retry
    def login(self, signature: str):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Logging into Talent Protocol..."
        )

        url = "https://login.talentprotocol.com/auth/wallet_login"

        chrome_version = get_browser_version(self.user_agent)

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://login.talentprotocol.com",
            "Priority": "u=1, i",
            "Referer": "https://login.talentprotocol.com/join",
            "Sec-Ch-Ua": f'"Chromium";v="{chrome_version}", "Not;A=Brand";v="24", "Google Chrome";v="{chrome_version}"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.user_agent,
        }

        payload = {
            "address": self.address,
            "chain_id": self.network.chain_id,
            "signature": signature,
        }

        response = requests.post(
            url=url, headers=headers, json=payload, proxies=self.default_proxies
        )

        if response.status_code == 200:
            return True

        raise

    def run_register(self):
        nonce = self.get_nonce()

        signature = self.sign_message(nonce=nonce)

        return self.login(signature=signature)
