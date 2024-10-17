from core.clients.evm_client import EvmClient
from core.clients.request_client import RequestClient
from core.utils.networks import Network, Networks
from core.utils.decorators import retry_execution
from web3 import Web3
from eth_account import Account
from typing import Self
from loguru import logger
from eth_typing import HexStr


class InstantBridge(RequestClient):
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        super().__init__(user_agent=user_agent, proxy=proxy)

        self.account_name = account_name
        self.private_key = private_key
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.account = Account.from_key(self.private_key)
        self.address = Web3.to_checksum_address(self.account.address)
        self.logger = logger
        self.module_name = "Zora Instant Bridge"
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_headers(self):

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://bridge.zora.energy",
            "Priority": "u=1, i",
            "Referer": "https://bridge.zora.energy/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "X-Rkc-Version": "1.11.2",
        }

        return headers

    def get_reservoir_bridge_tx(self, amount: int) -> tuple:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | {self.network.name} -> Zora Mainnet | Getting transaction..."
        )
        url = "https://api-zora.reservoir.tools/execute/call/v1"

        headers = self.get_headers()

        body = {
            "originChainId": self.client.chain_id,
            "txs": [{"data": "0x", "to": self.address, "value": str(int(amount))}],
            "user": self.address,
        }

        response = self.request_post(
            url=url,
            json=body,
            headers=headers,
        )

        return response

    @retry_execution
    def bridge(self, percentages: tuple[str, str]):

        amount = self.client.get_percentile(percentages=percentages)
        bridge_data = self.get_reservoir_bridge_tx(amount=amount)

        tx_info = bridge_data["steps"][0]["items"][0]["data"]

        act_value = int(tx_info["value"])
        tx_data = tx_info["data"]
        to_addr = tx_info["to"]

        bridge_tx_dict = self.client.get_tx_params(
            to_address=to_addr, value=act_value, data=tx_data, default_gas=200000
        )

        signed = self.client.sign_transaction(tx_dict=bridge_tx_dict)

        if signed:
            zora_client = EvmClient(
                account_name=self.account_name,
                private_key=self.private_key,
                network=Networks.Zora,
                user_agent=self.user_agent,
                proxy=self.proxy,
            )
            dst_bal_init = zora_client.get_eth_balance()

            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return self.client.wait_for_funds_on_dest_chain(
                    destination_network=Networks.Zora, original_balance=dst_bal_init
                )
        return
