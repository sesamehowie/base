from loguru import logger
from core.utils.custom_wrappers import exception_handler_with_retry
from core.utils.w3_manager import EthManager
from core.utils.networks import Network
from web3 import Web3
from eth_account import Account
from typing import Self
from eth_typing import HexStr


class SeasonalErosionNFT:
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
        self.account: Account = Account.from_key(self.private_key)
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
        self.module_name = "SeasonalErosionNFT"

        self.logger.debug(f"Now working: module {self.module_name}")

    @exception_handler_with_retry
    def mint(self):
        logger.info(f"{self.address} | {self.module_name} | Minting NFT...")

        data = (
            "0xa0712d680000000000000000000000000000000000000000000000000000000000000004"
        )
        value = 0
        to = Web3.to_checksum_address("0x2aa80a13395425EF3897c9684a0249a5226eA779")

        tx_params = self.client.get_tx_params(
            to_address=to, value=value, data=data, default_gas=200000
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)

            if res:
                return True

            return

        return
