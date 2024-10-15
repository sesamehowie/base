from web3 import Web3
from typing import Self
from loguru import logger
from eth_typing import HexStr
from eth_account import Account
from core.utils.networks import Network
from config import AAVE_CONTRACT, AAVE_WETH_CONTRACT, AAVE_ABI
from core.utils.helpers import sleeping
from core.utils.w3_manager import EthManager
from core.utils.custom_wrappers import exception_handler_with_retry


class Aave:
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
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.contract = self.client.get_contract(
            contract_addr=AAVE_CONTRACT, abi=AAVE_ABI
        )

        self.module_name = "Aave"
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.logger.debug(f"Now working: module {self.module_name}")

    def check_allowance(self, token_address: str, contract_address: str) -> int:
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.client.get_contract(contract_addr=token_address)
        amount_approved = contract.functions.allowance(
            self.address, contract_address
        ).call()

        return amount_approved

    @exception_handler_with_retry
    def approve(
        self, amount: int, token_address: str, contract_address: str
    ) -> bool | None:
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.client.get_contract(contract_addr=token_address)

        allowance_amount = self.check_allowance(token_address, contract_address)

        if amount > allowance_amount or amount == 0:
            logger.success(
                f"{self.account_name} | {self.address} | {self.module_name}| Approving..."
            )

            approve_amount = 2**128 if amount > allowance_amount else 0

            tx_data = {
                "from": self.address,
                "nonce": self.client.w3.eth.get_transaction_count(self.address),
                "chainId": self.network.chain_id,
            }

            transaction = contract.functions.approve(
                contract_address, approve_amount
            ).build_transaction(tx_data)

            signed = self.client.sign_transaction(tx_dict=transaction)

            if signed:

                txn_hash = self.client.send_tx(signed_tx=signed)
                sleeping(3)

                if txn_hash:
                    return True

                return

            return

    @exception_handler_with_retry
    def get_deposit_amount(self):
        aave_weth_contract = self.client.get_contract(contract_addr=AAVE_WETH_CONTRACT)

        amount = aave_weth_contract.functions.balanceOf(self.address).call()

        return amount

    @exception_handler_with_retry
    def deposit(
        self,
        min_amount: float,
        max_amount: float,
        decimal: int,
        make_withdraw: bool,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
    ) -> None:
        amount_wei, amount, balance = self.get_amount(
            "ETH", min_amount, max_amount, decimal, all_amount, min_percent, max_percent
        )

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Deposit: {amount} ETH"
        )

        tx_data = {
            "from": self.address,
            "nonce": self.client.w3.eth.get_transaction_count(self.address),
            "chainId": self.network.chain_id,
            "value": amount_wei,
        }

        transaction = self.contract.functions.depositETH(
            Web3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
            self.address,
            0,
        ).build_transaction(tx_data)

        signed = self.client.sign_transaction(transaction)

        if signed:
            tx_hash = self.send_raw_transaction(signed)
            if tx_hash:
                if make_withdraw:
                    sleeping(1)

                    self.withdraw()
                return
            return
        return

    @exception_handler_with_retry
    def withdraw(self) -> None:
        amount = self.get_deposit_amount()

        if amount > 0:
            self.logger.info(
                f"{self.account_name} | {self.address} | {self.module_name} | Withdraw: {self.w3.from_wei(amount, 'ether')} ETH"
            )

            self.approve(
                amount, "0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7", AAVE_CONTRACT
            )

            tx_data = {
                "from": self.address,
                "nonce": self.client.w3.eth.get_transaction_count(self.address),
                "chainId": self.network.chain_id,
            }

            transaction = self.contract.functions.withdrawETH(
                Web3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
                amount,
                self.address,
            ).build_transaction(tx_data)

            signed = self.client.sign_transaction(tx_dict=transaction)

            if signed:

                tx_hash = self.client.send_tx(signed_tx=signed)

                if tx_hash:
                    return True
                return

            return

        else:
            self.logger.warning(
                f"{self.account_name} | {self.address} | {self.module_name} | Deposit not found"
            )
            return
