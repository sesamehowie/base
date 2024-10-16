from loguru import logger
from core.utils.decorators import retry_execution
from core.clients.evm_client import EvmClient
from core.utils.networks import Network
from web3 import Web3
from eth_account import Account
from typing import Self
from eth_typing import HexStr
from core.modules.coinbase.coinbase_wallet_mints import Mints


class CityVerseNFT:
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
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "CityVerse NFT"

        self.logger.debug(f"Now working: module {self.module_name}")

    @retry_execution
    def mint(self):
        from config import CITYVERSE_CONTRACT_ADDR, CITYVERSE_PUBLIC_MINT_CALLDATA

        logger.info(f"{self.address} | {self.module_name} | Minting NFT...")

        data = CITYVERSE_PUBLIC_MINT_CALLDATA

        value = 0
        to = CITYVERSE_CONTRACT_ADDR

        tx_params = self.client.get_tx_params(
            to_address=to,
            value=value,
            data=data,
            default_gas=Mints.CityVerse.default_gas,
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)

            if res:
                return True

            return

        return
