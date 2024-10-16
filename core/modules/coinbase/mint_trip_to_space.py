from typing import Self
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from settings import REFERRAL_ADDR


class ANiceTripToSpace:
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        from config import ZORA_MINTER_ABI

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
        self.module_name = "A Nice Trip To Space"
        self.minter_addr = "0x777777722D078c97c6ad07d9f36801e653E356Ae"
        self.mint_addr = Web3.to_checksum_address(
            "0x849730870b6B9C82E9A8658748bDDD125a537D38"
        )
        self.ref = REFERRAL_ADDR
        self.token_id = 2
        self.qty = 1
        self.abi = ZORA_MINTER_ABI

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_data(self) -> str:
        contract = self.client.get_contract(
            contract_addr=self.minter_addr, abi=self.abi
        )

        data = contract.encodeABI(
            fn_name="mint",
            args=[self.address, self.qty, self.mint_addr, self.token_id, self.ref, ""],
        )

        return data

    @retry_execution
    def mint(self):
        data = self.get_data()

        value = Web3.to_wei(0.000111, "ether")

        tx_params = self.client.get_tx_params(
            to_address=self.minter_addr, value=value, data=data, default_gas=250000
        )

        signed = self.account.sign_transaction(tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)
            return res

        return
