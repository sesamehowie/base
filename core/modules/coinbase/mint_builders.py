from typing import Self
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from core.modules.coinbase.coinbase_wallet_mints import Mints


class BuildersNFT:
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
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "BuildersNFT"

        self.logger.debug(f"Now working: module {self.module_name}")

    @retry_execution
    def mint(self):
        from config import BUILDERS_ABI

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Starting mint..."
        )

        contract_addr = Web3.to_checksum_address(
            "0xc611fd3554a1ebf0e5eeD6F597DAaa50dA90FB08"
        )

        contract = self.client.get_contract(
            contract_addr=contract_addr, abi=BUILDERS_ABI
        )

        data = contract.encodeABI(fn_name="publicMint", args=[1])

        tx_dict = self.client.get_tx_params(
            to_address=contract_addr,
            value=Web3.to_wei(0.00077, "ether"),
            data=data,
            default_gas=Mints.SuperBasedBuilders.default_gas,
        )

        signed = self.client.sign_transaction(tx_dict=tx_dict)

        if signed:

            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

        return
