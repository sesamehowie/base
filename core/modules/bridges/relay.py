from loguru import logger
import requests
from core.clients.evm_client import EvmClient
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from web3 import Web3
from eth_account import Account
from typing import Self
from eth_typing import HexStr


class Relay:

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

        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )

        self.module_name = "Relay"

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_bridge_config(self, to_network: Network):
        from config import ZERO_ADDRESS

        url = "https://api.relay.link/config"

        headers = {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "referrer": "https://www.relay.link/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "user-agent": self.user_agent,
        }

        params = {
            "originChainId": self.client.network.chain_id,
            "destinationChainId": to_network.chain_id,
            "user": ZERO_ADDRESS,
            "currency": ZERO_ADDRESS,
        }

        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            proxies={"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"},
        )

        data = response.json()
        return data

    def get_bridge_data(self, amount_wei, to_network: Network):

        url = "https://api.relay.link/execute/call"

        payload = {
            "user": self.client.address,
            "txs": [{"to": self.client.address, "value": amount_wei, "data": "0x"}],
            "originChainId": self.network.chain_id,
            "destinationChainId": to_network.chain_id,
            "source": "relay.link",
        }

        response = requests.post(
            url=url,
            json=payload,
            headers={"User-Agent": self.user_agent},
            proxies={"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"},
        )

        data = response.json()
        return data

    @retry_execution
    def bridge(self, percentages: tuple[str, str], to_network: Network):
        from config import RELAY_CHAIN_NAME

        amount_in_wei = self.client.get_percentile(percentages=percentages)
        amount = self.client.get_human_amount(amount_in_wei)

        networks_data = self.get_bridge_config(to_network=to_network)
        tx_data = self.get_bridge_data(amount_wei=amount_in_wei, to_network=to_network)
        print(tx_data)
        print(networks_data)

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Bridge {round(amount, 6)}: {self.network.name} -> {RELAY_CHAIN_NAME[to_network.chain_id]}"
        )

        if networks_data["enabled"]:

            max_amount = networks_data["solver"]["capacityPerRequest"]

            if amount <= float(max_amount):
                dest_client = EvmClient(
                    account_name=self.account_name,
                    private_key=self.private_key,
                    network=to_network,
                    user_agent=self.user_agent,
                    proxy=self.proxy,
                )

                init_eth_balance = dest_client.get_eth_balance()

                to_address = tx_data["steps"][0]["items"][0]["data"]["to"]
                tx_data = tx_data["steps"][0]["items"][0]["data"]["data"]

                transaction = self.client.get_tx_params(
                    to_address=to_address,
                    value=amount_in_wei,
                    data=tx_data,
                    default_gas=200000,
                )

                signed = self.client.sign_transaction(tx_dict=transaction)

                if signed:

                    tx_hash = self.client.send_tx(signed_tx=signed)

                    if tx_hash:

                        return self.client.wait_for_funds_on_dest_chain(
                            destination_network=to_network,
                            original_balance=init_eth_balance,
                        )

                return
