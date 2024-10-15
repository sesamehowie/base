from loguru import logger
import requests
from core.utils.custom_wrappers import exception_handler_with_retry
from core.utils.networks import Network, Networks
from core.utils.w3_manager import EthManager
from settings import NITRO_FROM_TOKEN, NITRO_TO_TOKEN
from config import ETH_MASK
from web3 import Web3
from eth_account import Account
from typing import Self
from eth_typing import HexStr


class Nitro:
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
        self.network: Network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.module_name = "Nitro"

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_quote(
        self,
        to_network: Network,
        from_token_address: str,
        to_token_address: str,
        amount: int,
    ):
        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/quote"

        params = {
            "fromTokenAddress": from_token_address,
            "toTokenAddress": to_token_address,
            "amount": amount,
            "fromTokenChainId": self.client.chain_id,
            "toTokenChainId": str(to_network.chain_id),
            "partnerId": 1,
        }

        response = requests.get(
            url=url, params=params, headers=self.headers, proxies=self.default_proxies
        )

        data = response.json()

        return data

    def build_tx(self, quote: dict):
        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/transaction"

        quote |= {
            "receiverAddress": self.address,
            "senderAddress": self.address,
        }

        response = requests.post(
            url=url, headers=self.headers, json=quote, proxies=self.default_proxies
        )

        data = response.json()

        return data["txn"]["data"], self.client.w3.to_checksum_address(
            data["txn"]["to"]
        )

    @exception_handler_with_retry
    def bridge(
        self,
        percentages: tuple[str, str],
        to_network: Network = Networks.Ethereum,
        from_token_name: str = NITRO_FROM_TOKEN,
        to_token_name: str = NITRO_TO_TOKEN,
        from_token: str | None = ETH_MASK,
        to_token: str | None = ETH_MASK,
    ):

        amount = self.client.get_percentile(percentages=percentages)

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Sending {EthManager.get_human_amount(amount_wei=amount)} {from_token_name} from {self.client.network.name} for {to_token_name} in {to_network.name}"
        )

        dest_client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=to_network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )

        init_balance = dest_client.get_eth_balance()

        route_data = self.get_quote(to_network, from_token, to_token, amount)
        tx_data, to_address = self.build_tx(route_data)

        tx_params = self.client.get_tx_params(
            value=amount, to_address=to_address, data=tx_data, default_gas=200000
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return self.client.wait_for_funds_on_dest_chain(
                    destination_network=to_network, original_balance=init_balance
                )
