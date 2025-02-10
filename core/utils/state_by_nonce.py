from typing import Self
from loguru import logger
from eth_typing import HexStr
from eth_account import Account
from core.utils.networks import Network
from core.clients.evm_client import EvmClient
from core.utils.decorators import retry_execution


class StateByNonce(EvmClient):
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        super().__init__(
            account_name=account_name,
            private_key=private_key,
            network=network,
            user_agent=user_agent,
            proxy=proxy,
        )

        self.account_name = account_name
        self.private_key = private_key
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.account = Account.from_key(private_key)
        self.address = self.account.address

        self.module_name = "State by Nonce Checker"
        logger.debug(f"Now working: module {self.module_name}")

    @retry_execution
    def get_latest_nonce(self) -> int:
        logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Getting nonce on the latest block..."
        )

        return self.get_nonce(self.address)

    @retry_execution
    def get_nonce_by_block(self, block_num: int):
        logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Getting nonce on block {block_num}"
        )

        return self.w3.eth.get_transaction_count(self.address, block_num)

    def is_nonce_the_same_on_block(self, block_num: int) -> bool:
        logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Comparing nonces..."
        )

        latest_nonce = self.get_latest_nonce()
        nonce_on_block_num = self.get_nonce_by_block(block_num=block_num)

        if nonce_on_block_num == latest_nonce:
            logger.success(
                f"{self.account_name} | {self.address} | {self.module_name} | Nonces are the same!"
            )
            return True
        logger.warning(
            f"{self.account_name} | {self.address} | {self.module_name} | Nonces are not the same."
        )
        return False
