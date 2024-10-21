import json
from core.clients.request_client import RequestClient
from core.clients.evm_client import EvmClient
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from eth_typing import HexStr
from eth_account import Account
from web3 import Web3
from typing import Self
from loguru import logger
from decimal import Decimal
from settings import COINGECKO_API_KEY


class BalanceChecker(RequestClient):
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        super().__init__(user_agent=user_agent, proxy=proxy)

        self.logger = logger
        self.private_key = private_key
        self.account_name = account_name
        self.account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.module_name = "Balance Checker"
        self.client = EvmClient(
            account_name=account_name,
            private_key=private_key,
            network=network,
            user_agent=user_agent,
            proxy=proxy,
        )

        self.logger.debug(f"Now working: module {self.module_name}")

    @retry_execution
    def check_eth_balance(self) -> float:
        balance = self.client.get_eth_balance()

        return self.client.get_human_amount(amount_wei=balance)

    @staticmethod
    def eth_to_usd(amount_eth: float, usd_price: float) -> float:
        return round(amount_eth * usd_price, 2)

    @retry_execution
    def get_coingecko_token_price(self, token_id: str = "ethereum") -> float:
        url = f"https://api.coingecko.com/api/v3/coins/{token_id}"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": COINGECKO_API_KEY,
            "user-agent": self.user_agent,
        }

        data = self.request_get(url=url, headers=headers)

        return data["market_data"]["current_price"]["usd"]

    def run(self):
        eth_balance = self.check_eth_balance()

        usd_price = self.get_coingecko_token_price()

        usd_equivalent = self.eth_to_usd(amount_eth=eth_balance, usd_price=usd_price)

        logger.success(
            f"{self.account_name} - {self.address} - ETH balance: {eth_balance} ETH, to USD - {usd_equivalent}"
        )

        return True
