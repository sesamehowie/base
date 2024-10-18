import time
import random
from loguru import logger
from config import BASESWAP_ROUTER_ABI, BASESWAP_CONTRACTS, BASE_TOKENS, ERC20_ABI
from typing import Self
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
from eth_typing import HexStr
from core.utils.networks import Network
from core.utils.helpers import sleeping
from core.utils.decorators import retry_execution


class BaseSwap:
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
        self.module_name = "Baseswap"
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.swap_contract = self.client.get_contract(
            Web3.to_checksum_address(BASESWAP_CONTRACTS["router"]), BASESWAP_ROUTER_ABI
        )
        self.logger.debug(f"Now working: module {self.module_name}")

    def get_balance(self, contract_address: str) -> dict:
        contract_address = Web3.to_checksum_address(contract_address)
        contract = self.client.get_contract(contract_address, abi=ERC20_ABI)

        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(self.address).call()

        balance = balance_wei / 10**decimal

        return {
            "balance_wei": balance_wei,
            "balance": balance,
            "symbol": symbol,
            "decimal": decimal,
        }

    def get_amount(
        self,
        from_token: str,
        min_amount: float,
        max_amount: float,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
    ) -> list[int, float, float]:
        random_amount = round(random.uniform(min_amount, max_amount), decimal)
        random_percent = random.randint(min_percent, max_percent)

        percent = 1 if random_percent == 100 else random_percent / 100

        if from_token == "ETH":
            balance = self.client.get_eth_balance()
            amount_wei = (
                int(balance * percent)
                if all_amount
                else Web3.to_wei(random_amount, "ether")
            )

            amount = (
                Web3.from_wei(int(balance * percent), "ether")
                if all_amount
                else random_amount
            )
        else:
            balance = self.get_balance(BASE_TOKENS[from_token])
            amount_wei = (
                int(balance["balance_wei"] * percent)
                if all_amount
                else int(random_amount * 10 ** balance["decimal"])
            )
            amount = balance["balance"] * percent if all_amount else random_amount
            balance = balance["balance_wei"]

        return amount_wei, amount, balance

    def check_allowance(self, token_address: str, contract_address: str) -> int:
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.client.get_contract(contract_addr=token_address, abi=ERC20_ABI)
        amount_approved = contract.functions.allowance(
            self.address, contract_address
        ).call()

        return amount_approved

    def approve(
        self, amount: int, token_address: str, contract_address: str
    ) -> bool | None:
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.client.get_contract(contract_addr=token_address, abi=ERC20_ABI)

        allowance_amount = self.check_allowance(token_address, contract_address)

        if amount > allowance_amount or amount == 0:
            logger.success(
                f"{self.account_name} | {self.address} | {self.module_name} | Approving..."
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

    def get_min_amount_out(
        self, from_token: str, to_token: str, amount: int, slippage: float
    ):
        min_amount_out = self.swap_contract.functions.getAmountsOut(
            amount,
            [
                Web3.to_checksum_address(from_token),
                Web3.to_checksum_address(to_token),
            ],
        ).call()
        return int(min_amount_out[1] - (min_amount_out[1] / 100 * slippage))

    def swap_to_token(self, from_token: str, to_token: str, amount: int, slippage: int):
        tx_data = {
            "from": self.address,
            "nonce": self.client.w3.eth.get_transaction_count(self.address),
            "chainId": self.network.chain_id,
            "value": amount,
        }

        deadline = int(time.time()) + 10**6

        min_amount_out = self.get_min_amount_out(
            BASE_TOKENS[from_token], BASE_TOKENS[to_token], amount, slippage
        )

        contract_txn = self.swap_contract.functions.swapExactETHForTokens(
            min_amount_out,
            [
                Web3.to_checksum_address(BASE_TOKENS[from_token]),
                Web3.to_checksum_address(BASE_TOKENS[to_token]),
            ],
            self.address,
            deadline,
        ).build_transaction(tx_data)

        return contract_txn

    def swap_to_eth(self, from_token: str, to_token: str, amount: int, slippage: int):
        token_address = Web3.to_checksum_address(BASE_TOKENS[from_token])

        self.approve(amount, token_address, BASESWAP_CONTRACTS["router"])

        tx_data = self.get_tx_data()

        deadline = int(time.time()) + 1000000

        min_amount_out = self.get_min_amount_out(
            BASE_TOKENS[from_token], BASE_TOKENS[to_token], amount, slippage
        )

        contract_txn = self.swap_contract.functions.swapExactTokensForETH(
            amount,
            min_amount_out,
            [
                Web3.to_checksum_address(BASE_TOKENS[from_token]),
                Web3.to_checksum_address(BASE_TOKENS[to_token]),
            ],
            self.address,
            deadline,
        ).build_transaction(tx_data)

        return contract_txn

    @retry_execution
    def swap(
        self,
        from_token: str,
        to_token: str,
        min_amount: float,
        max_amount: float,
        decimal: int,
        slippage: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
    ):
        amount_wei, amount, balance = self.get_amount(
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent,
        )

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} Swap on BaseSwap – {from_token} -> {to_token} | {amount} {from_token}"
        )

        if from_token == "ETH":
            contract_txn = self.swap_to_token(
                from_token, to_token, amount_wei, slippage
            )
        else:
            contract_txn = self.swap_to_eth(from_token, to_token, amount_wei, slippage)

        signed = self.client.sign_transaction(contract_txn)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

            return

        return
