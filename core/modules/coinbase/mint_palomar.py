from typing import Self
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.modules.coinbase.coinbase_wallet_mints import Mints
from core.utils.decorators import retry_execution


class PalomarGroup:
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        from config import ZORA_BASE_1155_ABI

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
        self.module_name = Mints.PalomarGroup.name
        self.minter = "0x04E2516A2c207E84a1839755675dfd8eF6302F0a"
        self.minter_addr = "0xbCbEd193Fbc6bBA740607E64CC26042d052EBE85"
        self.token_id = 16
        self.qty = 1
        self.abi = ZORA_BASE_1155_ABI

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_data(self) -> str:
        from config import ZERO_ADDRESS

        contract = self.client.get_contract(
            contract_addr=self.minter_addr, abi=self.abi
        )

        data = contract.encodeABI(
            fn_name="mint",
            args=[
                self.minter,
                self.token_id,
                self.qty,
                [ZERO_ADDRESS],
                f"0x000000000000000000000000{self.address.lower()[2:]}",
            ],
        )

        return data

    @retry_execution
    def mint(self):
        data = self.get_data()

        value = Mints.PalomarGroup.mint_price

        tx_params = self.client.get_tx_params(
            to_address=self.minter_addr,
            value=value,
            data=data,
            default_gas=Mints.PalomarGroup.default_gas,
        )

        signed = self.account.sign_transaction(tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)
            return res

        return
