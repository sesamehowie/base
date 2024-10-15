from typing import Self
from eth_account import Account
from core.utils.w3_manager import EthManager
from web3 import Web3
import requests
from eth_typing import HexStr, ChecksumAddress
from loguru import logger
from core.utils.networks import Network
from core.utils.custom_wrappers import exception_handler_with_retry
from core.modules.coinbase.coinbase_wallet_mints import Mint, Mints


class CoinBasePointsManager:
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:

        self.logger = logger
        self.private_key = private_key
        self.account_name = account_name
        self.account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "CoinBase Points Manager"
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.state_url = f"https://basehunt.xyz/api/profile/state?userAddress={self.address}&gameId=2"
        self.completion_url = "https://basehunt.xyz/api/challenges/complete"

        self.logger.debug(f"Now working: module {self.module_name}")

    @exception_handler_with_retry
    def check_post_ocs_points(self) -> list[ChecksumAddress, int]:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Checking points for the Base Onchain Summer Campaign"
        )
        url = "https://basehunt.xyz/api/profile/statev2"

        payload = {"userAddress": self.address, "gameId": 2}

        response = requests.get(
            url=url,
            params=payload,
            headers=self.default_headers,
            proxies=self.default_proxies,
        ).json()
        try:
            if response["playedOCS"]:
                res = response["currentScore"]
            else:
                res = 0
            return [self.address, res]
        except (KeyError, ValueError):
            raise

    @exception_handler_with_retry
    def check_points(self) -> bool | None:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Checking points for the campaign..."
        )

        response = requests.get(
            url=self.state_url,
            headers=self.default_headers,
            proxies=self.default_proxies,
        )

        if response.status_code == 200:

            data = response.json()

            score = data["scoreData"]["currentScore"]

            self.logger.debug(
                f"{self.account_name} | {self.address} | {self.module_name} | Your score is {score}"
            )

            return True

        return

    @exception_handler_with_retry
    def collect_points(self, mint: Mint):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Collecting points for {mint.name} NFT..."
        )

        request_body = mint.get_point_data(wallet_address=self.address)

        response = requests.post(
            url=self.completion_url,
            headers=self.default_headers,
            json=request_body,
            proxies=self.default_proxies,
        )

        if response.status_code == 200:

            data = response.json()

            if data["success"]:
                return True

            return False

        return

    def check_and_claim(self):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Running checks to trigger points..."
        )

        for mint in Mints.AllMints:
            self.collect_points(mint=mint)

        self.check_points()

        return
