import random
from loguru import logger
from core.utils.decorators import retry_execution
from core.utils.networks import Network, Networks
from core.clients.evm_client import EvmClient
from core.clients.request_client import RequestClient
from settings import NITRO_FROM_TOKEN, NITRO_TO_TOKEN, NITRO_AMT_RANGE
from config import ETH_MASK
from eth_account import Account
from typing import Self
from eth_typing import HexStr


class Nitro(RequestClient):
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
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.network: Network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.client = EvmClient(
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

        data = self.request(url=url, method="GET", params=params, headers=self.headers)

        return data

    def build_tx(self, quote: dict):
        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/transaction"

        quote |= {
            "receiverAddress": self.address,
            "senderAddress": self.address,
        }

        data = self.request(
            url=url,
            method="POST",
            headers=self.headers,
            json=quote,
        )

        return data["txn"]["data"], self.client.w3.to_checksum_address(
            data["txn"]["to"]
        )

    @retry_execution
    def bridge(
        self,
        percentages: tuple[str, str] | None = None,
        amount_range: list[float, float] | None = NITRO_AMT_RANGE,
        to_network: Network = Networks.Ethereum,
        from_token_name: str = NITRO_FROM_TOKEN,
        to_token_name: str = NITRO_TO_TOKEN,
        from_token: str | None = ETH_MASK,
        to_token: str | None = ETH_MASK,
    ):

        if percentages:
            amount = self.client.get_percentile(percentages=percentages)
            amount_float = self.client.get_human_amount(amount_wei=amount)
        elif amount_range:
            amount_float = round(random.uniform(amount_range[0], amount_range[1]), 6)
            amount = self.client.to_wei(amount=amount_float, decimals=18)

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Sending {amount_float} {from_token_name} from {self.client.network.name} for {to_token_name} in {to_network.name}"
        )

        dest_client = EvmClient(
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
