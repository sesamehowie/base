from core.clients.evm_client import EvmClient
from core.utils.networks import Network, Networks
from core.utils.decorators import retry_execution
import time
from eth_typing import HexStr
from eth_account import Account
from web3 import Web3
from web3.types import Wei
from typing import Dict, Tuple, Self
from loguru import logger


class SmartL2Checker:
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
        self.module_name = "Smart L2 Network Selector"

        self.logger.debug(f"Now working: module {self.module_name}")

        self.networks: Tuple[Network] = (
            Networks.Arbitrum,
            Networks.Optimism,
            Networks.Linea,
        )

        self.networks_mapping: Dict[str, Network] = {
            "Base": Networks.Base,
            "Arbitrum": Networks.Arbitrum,
            "Optimism": Networks.Optimism,
            "Linea": Networks.Linea,
        }

    @retry_execution
    def get_runner_network(self) -> Network:
        total_map: Dict = dict()

        max_val: int | Wei = 0

        for network in self.networks:

            manager = EvmClient(
                account_name=self.account_name,
                private_key=self.private_key,
                network=network,
                user_agent=self.user_agent,
                proxy=self.proxy,
            )

            balance: Wei = manager.get_eth_balance()
            total_map |= [(network.name, balance)]
            time.sleep(10)

            if balance >= max_val:
                max_val = balance

        for k, v in list(total_map.items()):
            if v == max_val:
                return self.networks_mapping[k]
