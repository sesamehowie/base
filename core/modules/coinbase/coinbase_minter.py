from typing import Self
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
from requests import Session
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from core.modules.coinbase.coinbase_wallet_mints import Mint


class CoinbaseMinter:
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
        self.session = Session()
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.session.headers.update({"User-Agent": self.user_agent})
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.module_name = "Coinbase Minter"

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_tx_data(self, mint: Mint) -> str | None:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Getting transaction data for {mint.name} NFT..."
        )
        contract = self.client.get_contract(
            contract_addr=mint.mint_address, abi=mint.abi
        )
        function_name = mint.type.function_name
        input_data = mint.type.get_interface(self.address, mint.mint_price)
        if mint.type.type_id != 1:
            return input_data

        data = contract.encodeABI(fn_name=function_name, args=input_data)
        return data

    @retry_execution
    def mint(self, mint: Mint):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Starting mint run for {mint.name} NFT..."
        )

        if not mint.is_active:
            logger.warning(
                f"{self.account_name} | {self.address} | {self.module_name} | Mint of {mint.name} is deprecated, skipping..."
            )
            return True

        to_addr = mint.mint_address
        value = mint.mint_price
        data = self.get_tx_data(mint=mint)

        tx_params = self.client.get_tx_params(
            to_address=to_addr, data=data, value=value, default_gas=mint.default_gas
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

            return False

        return
